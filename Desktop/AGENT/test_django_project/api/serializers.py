from rest_framework import serializers
from .models import User, Post


class UserSerializer(serializers.ModelSerializer):
    """Class: function"""
    class Meta:
        """Class: function"""
        model = User
        fields = ['id', 'name', 'email', 'created_at', 'age']
        read_only_fields = ['id', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    """Class: function"""
    class Meta:
        """Class: function"""
        model = Post
        fields = ['id', 'user_id', 'title', 'body', 'created', 'likes']
