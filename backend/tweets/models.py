from django.db import models
from django.contrib.auth.models import User


class Tweet(models.Model):
    """
        The tweet model
    """
    user = models.ForeignKey(User)
    text = models.CharField(max_length=150)
    image_url = models.CharField(max_length=100, null=True, blank=True)
    video_url = models.CharField(max_length=100, null=True, blank=True)
