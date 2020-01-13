from rest_framework import status
from django.test import TestCase, Client
from posts.models import User

client = Client()


class TestToken(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('admin', 'vasia.duba@gmail.com', '1111')
        self.tokens = client.post('/api/v1/token/', data={'username': self.user.username, 'password': '1111'}).data

    def test_token_with_blank_credentials(self):
        response = client.post('/api/v1/token/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_with_invalid_credentials(self):
        response = client.post('/api/v1/token/', data={'username': 'admin', 'password': '1110'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_with_valid_credentials(self):
        response = client.post('/api/v1/token/', data={'username': 'admin', 'password': '1111'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_refresh(self):
        response = client.post('/api/v1/token/refresh/', data={'refresh': self.tokens['refresh']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestSignup(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('admin', 'vasia.duba@gmail.com', '1111')
        self.tokens = client.post('/api/v1/token/', data={'username': self.user.username, 'password': '1111'}).data

    def test_blank_signup(self):
        response = client.post('/api/v1/signup/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_username(self):
        response = client.post('/api/v1/signup/', data={
            'username':'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'email': 'vasia.duba@gmail.com',
            'password': '1234',
            'password2': '1234'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['username'], ["Ensure this field has no more than 150 characters."])

    def test_different_passwords(self):
        response = client.post('/api/v1/signup/', data={
            'username': 'abcd',
            'email': 'vasia.duba@gmail.com',
            'password': '1234',
            'password2': '1235'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['password'], "Passwords must match.")

    def test_existing_username(self):
        response = client.post('/api/v1/signup/', data={
            'username': 'admin',
            'email': 'vasia123.duba@gmail.com',
            'password': '1234',
            'password2': '1234'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['username'], ["A user with that username already exists."])

    def test_invalid_email(self):
        response = client.post('/api/v1/signup/', data={
            'username': 'abcd',
            'email': '1234',
            'password': '1234',
            'password2': '1234'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'], ["Enter a valid email address."])

    def test_valid_signup(self):
        response = client.post('/api/v1/signup/', data={
            'username': 'abcd',
            'email': 'vasia123.duba@gmail.com',
            'password': '1234',
            'password2': '1234'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {"username": "abcd", "email": "vasia123.duba@gmail.com"})


class TestLogin(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('admin', 'vasia.duba@gmail.com', '1111')
        self.tokens = client.post('/api/v1/token/', data={'username': self.user.username, 'password': '1111'}).data

    def test_valid_login(self):
        response = client.get('/api/v1/login/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post('/api/v1/login/', data={'username': 'admin', 'password': '1111'})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_invalid_login(self):
        response = client.post('/api/v1/login/', data={'username': 'admin', 'password': '1411'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
