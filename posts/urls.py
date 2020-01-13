from django.contrib import admin
from django.urls import path, include
from posts.views import *

app_name = 'posts'
urlpatterns = [
    path('posts/all/', PostListView.as_view()),
    path('posts/create/', PostCreateView.as_view()),
    path('posts/like/<int:pk>', PostLikeView.as_view()),
    path('posts/unlike/<int:pk>', PostUnlikeView.as_view())
]
