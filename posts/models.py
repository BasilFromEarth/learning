from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    title = models.CharField(verbose_name="Title", max_length=128)
    text = models.CharField(verbose_name="Text", max_length=10240)
    creation_date = models.DateTimeField(verbose_name="Created", auto_now=True)
    likes = models.IntegerField(verbose_name="Likes", default=0)
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
