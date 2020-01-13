import clearbit

from pyhunter import PyHunter
from rest_framework import serializers
from posts.models import Post, User

clearbit.key = 'sk_9901bd8e1e154c0204fdef9a2818d52d'
hunter = PyHunter('382e59a92fbd6a48670a24a84908663251cd94ab')


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'likes')


class PostDetailSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = '__all__'


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'likes')
        extra_kwargs = {
            'title': {'read_only': True},
            'likes': {'read_only': True}
        }

    def update(self, instance, validated_data):
        instance.likes += 1
        instance.save()
        return instance


class PostUnlikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'likes')
        extra_kwargs = {
            'title': {'read_only': True},
            'likes': {'read_only': True}
        }

    def update(self, instance, validated_data):
        instance.likes -= 1
        instance.save()
        return instance


class SignupSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {
            'password': {'style': {'input_type': 'password'}, 'write_only': True}
        }

    def save(self, **kwargs):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']


        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        elif user.email:
            if not hunter.email_verifier(user.email):
                raise serializers.ValidationError({'email': 'Email must be real.'})

        lookup = clearbit.Enrichment.find(email=user.email, stream=True)
        if lookup:
            user.first_name = lookup['person']['name']['givenName']
            user.last_name = lookup['person']['name']['familyName']

        user.set_password(password)
        user.save()
        return user

