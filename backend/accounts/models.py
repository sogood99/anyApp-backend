from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
        A profile class containing all necessary other information for user
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    profileName = models.CharField(max_length=20)
    userIconUrl = models.CharField(max_length=100, blank=True, null=True)
    userBkgUrl = models.CharField(max_length=100, blank=True, null=True)
    createDate = models.DateTimeField(auto_now_add=True)
    profileInfo = models.CharField(max_length=150, blank=True, null=True)
