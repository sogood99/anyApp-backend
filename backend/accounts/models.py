from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, F


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


class Follow(models.Model):
    """
        Follow model
        @param user User that followed
        @param user User that is being followed
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False, related_name='user')
    followedUser = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False, related_name='follwed_user')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'followedUser'], name='unique-user-follow'
            ),
            models.CheckConstraint(
                check=~Q(user=F('followedUser')), name='cannot-follow-self'
            )
        ]
