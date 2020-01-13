from django.shortcuts import render
from rest_framework import generics
from posts.serializers import *
from posts.models import Post
from rest_framework.permissions import IsAuthenticated


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostDetailSerializer
    permission_classes = (IsAuthenticated,)


class PostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated,)


class PostLikeView(generics.UpdateAPIView):
    serializer_class = PostLikeSerializer
    queryset = Post.objects.all()


class PostUnlikeView(generics.UpdateAPIView):
    serializer_class = PostUnlikeSerializer
    queryset = Post.objects.all()


class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer




