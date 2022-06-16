from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.fields import empty
from django.contrib.auth.models import User

from accounts.models import Profile
from tweets.models import Tweet, Like


class TweetSerializer(serializers.ModelSerializer):

    def __init__(self, user=None, instance=None, data=empty, **kwargs):
        super().__init__(instance, data, **kwargs)
        self.user = user

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
    likes = serializers.SerializerMethodField('getLikeCount', read_only=True)
    isLiked = serializers.SerializerMethodField(
        'getIfUserLiked', read_only=True)

    class Meta:
        model = Tweet
        fields = ('tweetId', 'userId', 'username', 'userIconUrl',
                  'text', 'imageUrl', 'videoUrl', 'repliesId', 'createDate', 'likes', 'isLiked')

    def getUserIconUrl(self, obj):
        userProfile = Profile.objects.get(pk=obj.user)
        if userProfile is not None and userProfile.userIconUrl is not None:
            return userProfile.userIconUrl
        else:
            return 'image/userIcon/default.jpg'

    def getLikeCount(self, obj):
        likeCount = Like.objects.filter(tweet=obj).count()
        return likeCount

    def getIfUserLiked(self, obj):
        if self.user is None or self.user.is_authenticated:
            likeCount = Like.objects.filter(user=self.user, tweet=obj).count()
            return (likeCount > 0)
        return False


class LikeSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(source='id',
    #                                           read_only=False, queryset=User.objects.all())
    # tweet = serializers.PrimaryKeyRelatedField(source='id',
    #                                            read_only=False, queryset=Tweet.objects.all())

    class Meta:
        model = Like
        fields = ('user', 'tweet')
