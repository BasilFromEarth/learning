from rest_framework import status
from django.test import TestCase, Client
from posts.models import User, Post
from posts.serializers import *

client = Client()


class TestPost(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('admin', 'vasia.duba@gmail.com', '1111')
        self.tokens = client.post('/api/v1/token/', data={'username': self.user.username, 'password': '1111'}).data
        Post.objects.create(title='1', text='1', user=self.user)
        Post.objects.create(title='2', text='2', user=self.user)
        Post.objects.create(title='3', text='3', user=self.user)

    def test_post_get_all(self):
        response = client.get('/api/v1/posts/all/', HTTP_AUTHORIZATION='Bearer ' + self.tokens['access'])
        serializer = PostListSerializer(Post.objects.all(), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)


    def test_post_create(self):
        response = client.post('/api/v1/posts/create/', data={'text': '5', 'title': '5'}, HTTP_AUTHORIZATION='Bearer ' + self.tokens['access'])
        serializer = PostDetailSerializer(Post.objects.get(text='5'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(serializer.data, response.data)

    def test_post_likes(self):
        post = Post.objects.get(id=1)
        response = client.put('/api/v1/posts/like/1')
        post.likes += 1
        serializer = PostLikeSerializer(post)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

        response = client.put('/api/v1/posts/unlike/1')
        post.likes -= 1
        serializer = PostLikeSerializer(post)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)
