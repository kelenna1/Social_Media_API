from django.urls import path, include
from django.contrib import admin
from .views import UserProfileView, UserRegistrationView, PostListCreateView,FollowView,UnfollowView, PostDetailView, FeedView, LikeView, CommentView

urlpatterns = (
    path('register', UserRegistrationView.as_view(), name ='user-register'),
    path('profile',UserProfileView.as_view(), name = 'user-profile'),
    path('posts', PostListCreateView.as_view(), name='posts'),
    path('posts/<int:pk>', PostDetailView.as_view(), name= 'post-detail'),
    path('follow', FollowView.as_view(), name='follow-user'),
    path('unfollow/int:pk/', UnfollowView.as_view(), name='unfollow-user'),
    path('posts/<int:pk>/like/', LikeView.as_view(), name='like-post'), 
    path('posts/<int:pk>/comments/', CommentView.as_view(), name='comment-post'),
    path('feed', FeedView.as_view(), name='feed'),
)