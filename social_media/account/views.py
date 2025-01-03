from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import status
from .serializers import UserRegistrationSerializer, UserSerializer, UserProfileSerializer, PostSerializer, FollowSerializer,LikeSerializer, CommentSerializer
from .models import User, Post,Follow, Like, Comment
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Save the user
            # Generate tokens for the new user
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User registered successfully!",
                "user": {
                    "username": user.username,
                    "email": user.email,
                },
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class TokenLoginView(APIView):
#     serializer_class = 
#     permission_classes = [AllowAny]

#     def get(self, request):
#         user = request.user
#         return Response({
#             "message": "Login successful",
#             "username": user.username,
#             "email": user.email,
#         }, status=200)
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        serializer = UserProfileSerializer( request.user, data=request.data, partial = True,)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PostListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        posts = Post.objects.all().order_by('-timestamp')
        serializer = PostSerializer(posts, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author= request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        post = get_object_or_404(Post, pk=pk)
        if post.author != user:
            return None
        return post
    
    def put(self, request, pk):
        post = self.get_object(pk, request.user)
        if not post:
            return Response({"detail": "Not authorized to update this message"}, status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(post, data=request.data, partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk,request.user, )
        if not post:
            return Response({"detail": "Not authorized to delete this message"}, status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response({"detail": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
# class FollowView(CreateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = FollowSerializer

#     def perform_create(self, serializer):
#         following = User.objects.get(id=self.request.data.get('following'))
#         if following == self.request.user:
#             raise ValidationError("You cannot follow yourself")
#         serializer.save(follower = self.request.user)

class FollowView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
        try:
            following = User.objects.get(id=self.request.data.get('following'))
        except User.DoesNotExist:
            raise ValidationError({"error": "User not found."})

        if following == self.request.user:
            raise ValidationError({"error": "You cannot follow yourself."})

        if Follow.objects.filter(follower=self.request.user, following=following).exists():
            raise ValidationError({"error": "You are already following this user."})

        serializer.save(follower=self.request.user)

# class UnfollowView(DestroyAPIView):
#     permission_classes = [IsAuthenticated]

#     def delete(self, request, *args, **kwargs):
#         following = User.objects.get(id=kwargs['pk'])
#         follow_instance = Follow.objects.filter(follower = request.user, following=following).first()
#         if not follow_instance:
#             return Response({"error": "you are not following this user."}, status=status.HTTP_400_BAD_REQUEST)
#         follow_instance.delete()
#         return Response({"message": "You've successfully unfollowed "}, status=status.HTTP_200_OK)

class UnfollowView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        try:
            following = User.objects.get(id=kwargs['pk'])
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        follow_instance = Follow.objects.filter(follower=request.user, following=following).first()
        if not follow_instance:
            return Response({"error": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)

        follow_instance.delete()
        return Response({"message": "You have successfully unfollowed the user."}, status=status.HTTP_200_OK)

class FeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        following = Follow.objects.filter(follower=user).values_list('following', flat=True)
        posts = Post.objects.filter(author__in = list(following) + [user]).order_by('-timestamp')

        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(posts, request)

        serializer = PostSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class LikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()  # Toggle functionality
            return Response({"message": "Like removed"}, status=status.HTTP_200_OK)
        return Response({"message": "Post liked"}, status=status.HTTP_201_CREATED)

# class CommentView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, pk):
#         post = Post.objects.get(pk=pk)
#         serializer = CommentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user, post=post)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get(self, request, pk):
#         post = Post.objects.get(pk=pk)
#         comments = post.comments.all()
#         serializer = CommentSerializer(comments, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework.exceptions import NotFound

class CommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound("Post not found")
        
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            # Automatically set user and post when saving
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound("Post not found")
        
        comments = post.comments.all()  # Assuming a reverse relationship `post.comments`
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
