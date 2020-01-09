from django.contrib import admin
from django.urls import path, include
from posts.views import *

app_name = 'posts'
urlpatterns = [
    path('post/create/', PostCreateView.as_view()),
    path('all/', PostListView.as_view()),
    path('post/detail/<int:pk>', PostLikesView.as_view())
]
