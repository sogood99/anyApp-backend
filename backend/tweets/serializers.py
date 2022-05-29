from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

from tweets.models import Tweet


class TweetSerializer(serializers.ModelSerializer):
    tweetId = serializers.IntegerField(source='id')
    userId = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')
    text = serializers.CharField()
    imageUrl = serializers.CharField()
    videoUrl = serializers.CharField()
    repliesId = serializers.IntegerField()
    createDate = serializers.DateTimeField()

    class Meta:
        model = Tweet
        fields = ('tweetId', 'userId', 'username',
                  'text', 'imageUrl', 'videoUrl', 'repliesId', 'createDate')
