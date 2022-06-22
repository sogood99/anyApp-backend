from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

from .models import Block, Follow, Notification, Profile


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(required=False,
                                     validators=[UniqueValidator(
                                         queryset=User.objects.all())],
                                     max_length=32)
    password = serializers.CharField(required=True,
                                     min_length=6,
                                     write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True)
    userId = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    profileName = serializers.CharField(max_length=20, default="User")
    userIconUrl = serializers.SerializerMethodField(
        'getUserIconUrl', read_only=True)
    userBkgUrl = serializers.SerializerMethodField(
        'getUserBkgUrl', read_only=True)
    createDate = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")
    profileInfo = serializers.CharField(
        max_length=150, default=None, allow_null=True)

    class Meta:
        model = Profile
        fields = ('user', 'userId', 'username', 'profileName', 'userIconUrl',
                  'userBkgUrl', 'createDate', 'profileInfo')

    def getUserIconUrl(self, obj):
        if obj.userIconUrl == None:
            return 'image/userIcon/default.jpg'
        else:
            return obj.userIconUrl

    def getUserBkgUrl(self, obj):
        if obj.userBkgUrl == None:
            return 'image/userBkgImg/default.jpg'
        else:
            return obj.userBkgUrl


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ('user', 'followedUser')


class BlockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Block
        fields = ('user', 'blockedUser')


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ('user', 'type', 'createDate', 'tweetId', 'tweetBrief',
                  'likeUserId', 'likeUserInfo', 'followUserId', 'followUserInfo', 'replyTweetId', 'replyTweetBrief')
