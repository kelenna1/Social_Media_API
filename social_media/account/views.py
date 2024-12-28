from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .serializers import UserRegistrationSerializer, UserSerializer, UserProfileSerializer, PostSerializer, FollowSerializer
from .models import User, Post,Follow
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
# Create your views here.

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response( {"message": "User created succesfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
    permission_classes = [IsAuthenticated]

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
        post = self.get_object(pk,request.user, partial=True)
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
