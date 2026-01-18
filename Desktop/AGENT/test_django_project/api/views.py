from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Post
from .serializers import UserSerializer, PostSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Class: function"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'])
    def get_user_posts(self, request, pk=None):
        """Function: function"""
        user = self.get_object()
        posts = Post.objects.filter(user_id=user.id)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    """Class: function"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def clean(self):
        """Validate model fields."""
        if self.age and not self.age > 0 and self.age < 150:
            raise ValueError(f"Invalid age")
