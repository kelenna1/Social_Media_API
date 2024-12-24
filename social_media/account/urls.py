from django.urls import path, include
from django.contrib import admin
from .views import UserProfileView, UserRegistrationView

urlpatterns = (
    path('register', UserRegistrationView.as_view(), name ='user-register'),
    path('profile',UserProfileView.as_view(), name = 'user-profile'),
)