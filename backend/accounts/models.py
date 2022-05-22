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
    profile_name = models.CharField(max_length=20)
    create_date = models.DateTimeField(auto_now_add=True)
