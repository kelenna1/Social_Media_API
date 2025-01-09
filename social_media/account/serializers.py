from rest_framework import serializers
from .models import User, Post, Follow, Like, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture']
        read_only_fields = ['id']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, min_length=8)

    class Meta:
        model= User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):

        user = User.objects.create_user(
            username= validated_data['username'],
            email= validated_data['email'],
            password= validated_data['password'],
        )
        return user
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'profile_picture']

class PostSerializer(serializers.ModelSerializer):
    #That the author brings out the username instead of the user id
    author =serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Post
        fields= ['id', 'content', 'author', 'timestamp', 'media', ]
        read_only_fields = ['author', 'timestamp']
        

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'following', 'follower', 'created_at']
        read_only_fields = ['follower', 'created_at']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'timestamp']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'timestamp']
