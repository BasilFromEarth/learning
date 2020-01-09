from django.shortcuts import render
from rest_framework import generics
from posts.serializers import PostDetailSerializer, PostListSerializer
from posts.models import Post
from rest_framework.permissions import IsAuthenticated


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostDetailSerializer


class PostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()


class PostLikesView(generics.RetrieveUpdateAPIView):
    serializer_class = PostDetailSerializer
    queryset = Post.objects.all()
    permission_classes = (IsAuthenticated, )



