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
    profileName = serializers.SerializerMethodField(
        'getProfileName', read_only=True)
    userIconUrl = serializers.SerializerMethodField(
        'getUserIconUrl', read_only=True)
    text = serializers.CharField()
    imageUrl = serializers.CharField()
    videoUrl = serializers.CharField()
    audioUrl = serializers.CharField()
    location = serializers.CharField()
    repliesId = serializers.SerializerMethodField(
        'getRepliesId', read_only=True)
    createDate = serializers.DateTimeField()
    likes = serializers.SerializerMethodField('getLikeCount', read_only=True)
    isLiked = serializers.SerializerMethodField(
        'getIfUserLiked', read_only=True)
    isSelf = serializers.SerializerMethodField('getIfSelf', read_only=True)

    class Meta:
        model = Tweet
        fields = ('tweetId', 'userId', 'username', 'location', 'profileName', 'userIconUrl',
                  'text', 'imageUrl', 'videoUrl', 'audioUrl', 'repliesId', 'createDate', 'likes', 'isLiked', 'isSelf')

    def getUserIconUrl(self, obj):
        userProfile = Profile.objects.get(pk=obj.user)
        if userProfile is not None and userProfile.userIconUrl is not None:
            return userProfile.userIconUrl
        else:
            return 'image/userIcon/default.jpg'

    def getProfileName(self, obj):
        userProfile = Profile.objects.get(pk=obj.user)
        if userProfile is not None and userProfile.profileName is not None:
            return userProfile.profileName
        else:
            return 'UserError'

    def getRepliesId(self, obj):
        if obj.repliesTweet != None:
            return obj.repliesTweet.id
        else:
            return None

    def getLikeCount(self, obj):
        likeCount = Like.objects.filter(tweet=obj).count()
        return likeCount

    def getIfUserLiked(self, obj):
        if self.user is None or self.user.is_authenticated:
            likeCount = Like.objects.filter(user=self.user, tweet=obj).count()
            return (likeCount > 0)
        return False

    def getIfSelf(self, obj):
        if self.user is None or self.user.is_authenticated:
            return self.user == obj.user
        return False


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('user', 'tweet')
