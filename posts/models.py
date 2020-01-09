from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    title = models.CharField(verbose_name="Title", max_length=128)
    text = models.CharField(verbose_name="Text")
    likes = models.IntegerField(verbose_name="Likes")
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
