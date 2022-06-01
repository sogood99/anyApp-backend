from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

from accounts.models import Profile
from tweets.models import Tweet


class TweetSerializer(serializers.ModelSerializer):
    tweetId = serializers.IntegerField(source='id', read_only=True)
    userId = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    userIconUrl = serializers.SerializerMethodField(
        'getUserIconUrl', read_only=True)
    text = serializers.CharField()
    imageUrl = serializers.CharField()
    videoUrl = serializers.CharField()
    repliesId = serializers.IntegerField()
    createDate = serializers.DateTimeField()

    class Meta:
        model = Tweet
        fields = ('tweetId', 'userId', 'username', 'userIconUrl',
                  'text', 'imageUrl', 'videoUrl', 'repliesId', 'createDate')

    def getUserIconUrl(self, obj):
        userProfile = Profile.objects.get(pk=obj.user)
        if userProfile is not None and userProfile.userIconUrl is not None:
            return userProfile.userIconUrl
        else:
            return 'image/userIcon/default.jpg'
