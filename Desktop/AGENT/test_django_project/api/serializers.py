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

    def clean(self):
        """Validate model fields."""
        if self.age and not self.age > 0 and self.age < 150:
            raise ValueError(f"Invalid age")
