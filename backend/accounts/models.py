from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, F

from tweets.models import Tweet


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
        @param followedUser User that is being followed
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False, related_name='f_user')
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


class Block(models.Model):
    """
        Block model
        @param user User that blocked
        @param blockedUser User that is being blocked
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False, related_name='b_user')
    blockedUser = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False, related_name='blocked_user')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'blockedUser'], name='unique-user-block'
            ),
            models.CheckConstraint(
                check=~Q(user=F('blockedUser')), name='cannot-block-self'
            )
        ]


class Notification(models.Model):
    """
        Block model
        @param user : For which user
        @param type : Type of notifications (Like, Follow, Reply)
        @param createDate : Date which the tweet got dispatched
        @param tweetId : Tweet which got liked/replied
        @param likeUserId : User which liked the tweet
        @param followUserId : User which followed user
        @param replyTweetId : User which followed user
        @param replyUserId : User which followed user
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=False, null=False, related_name='notification_user')
    type = models.CharField(blank=True, null=True, max_length=32)
    createDate = models.DateTimeField(auto_now_add=True)
    tweetId = models.ForeignKey(
        Tweet, on_delete=models.CASCADE, blank=True, null=True, related_name='notification_tweet_id')
    likeUserId = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name='liked_user_id')
    followUserId = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name='follow_user_id')
    replyTweetId = models.ForeignKey(
        Tweet, on_delete=models.CASCADE, blank=True, null=True, related_name='reply_tweet_id')
