from django.db import models
from django.contrib.auth.models import User


class Tweet(models.Model):
    """
        The tweet model
        @param user User that send the tweet
        @param text Text field of the tweet
        @param imageUrl Url for image (nullable)
        @param videoUrl Url for video (nullable)
        @param audioUrl Url for audio (nullable)
        @param repliesTweet If this tweet is a reply of another tweet, foriegn key ref that tweet
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=150, blank=True)
    imageUrl = models.CharField(max_length=100, null=True, blank=True)
    videoUrl = models.CharField(max_length=100, null=True, blank=True)
    audioUrl = models.CharField(max_length=100, null=True, blank=True)
    repliesTweet = models.ForeignKey(
        "Tweet", on_delete=models.CASCADE, null=True, blank=True)
    createDate = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    """
        Like model
        @param user User that liked
        @param tweet Tweet that the user liked
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False)
    tweet = models.ForeignKey(
        Tweet, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'tweet'], name='unique_like_for_user_tweet'
            )
        ]
