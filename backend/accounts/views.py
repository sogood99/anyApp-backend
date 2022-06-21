from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from . import serializers, models


class UserCreate(APIView):
    """
        Creates a user
    """

    def post(self, request, format='json'):
        user_serializer = serializers.UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            if user:
                # Create a Profile Model
                profile_json = {'user': user.id, 'profileName': 'User ' +
                                str(user.id), 'profileInfo': None}
                profile_serializer = serializers.ProfileSerializer(
                    data=profile_json)
                if profile_serializer.is_valid():
                    profile = profile_serializer.save()
                    if profile:
                        token = Token.objects.create(user=user)
                        json = user_serializer.data
                        json['token'] = token.key
                        return Response(json, status=status.HTTP_201_CREATED)
                user.delete()
                return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdate(APIView):
    """
        Update a user
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format='json'):

        if 'password' not in request.data or 'newPassword' not in request.data:
            return Response('Please include Username Password Not Found', status=status.HTTP_400_BAD_REQUEST)

        user: User = request.user

        if not user.check_password(request.data['password']):
            return Response('Incorrect Password', status=status.HTTP_401_UNAUTHORIZED)

        user.set_password(request.data['newPassword'])
        user.save()

        return Response('Set password success', status=status.HTTP_200_OK)


class GetProfileJson(APIView):
    """
        Get Profile Information
    """

    def get(self, request):
        if request.user.is_authenticated:
            profile = models.Profile.objects.get(pk=request.user)
            if profile:
                profile_serializer = serializers.ProfileSerializer(
                    instance=profile)
                return Response(profile_serializer.data)
        return Response('Not Authenticated', status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format='json'):
        if 'userId' in request.data:
            requestUserId = request.data['userId']
            profile = models.Profile.objects.get(pk=requestUserId)
            if profile:
                profile_serializer = serializers.ProfileSerializer(
                    instance=profile)
                # check if user is self
                jsonResp = profile_serializer.data
                if request.user.is_authenticated and request.user == profile.user:
                    jsonResp['isSelf'] = True
                else:
                    jsonResp['isSelf'] = False

                    # check if followed requestUser
                    if request.user.is_authenticated:
                        user = request.user
                        targetUser = User.objects.get(pk=requestUserId)

                        follow = models.Follow.objects.filter(
                            user=user, followedUser=targetUser).first()
                        if follow is not None:
                            jsonResp['isFollowed'] = True
                        else:
                            jsonResp['isFollowed'] = False

                        block = models.Block.objects.filter(
                            user=user, blockedUser=targetUser).first()
                        if block is not None:
                            jsonResp['isBlocked'] = True
                        else:
                            jsonResp['isBlocked'] = False
                    else:
                        jsonResp['isFollowed'] = False
                        jsonResp['isBlocked'] = False

                return Response(jsonResp)

        return Response('User Not Found', status=status.HTTP_400_BAD_REQUEST)


class UpdateProfile(APIView):

    """
        Updates User Profile
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format='json'):
        profile = models.Profile.objects.get(pk=request.user)

        if 'profileName' in request.data:
            profile.profileName = request.data['profileName']

        if 'profileInfo' in request.data:
            profile.profileInfo = request.data['profileInfo']

        if 'userIcon' in request.FILES:
            image = request.FILES['userIcon']
            ext = image.name.split('.')[-1]
            imageUrl = default_storage.save(
                'image/userIcon/' + str(request.user.id) + '.' + ext, ContentFile(image.read()))
            profile.userIconUrl = imageUrl

        if 'userBkgImg' in request.FILES:
            image = request.FILES['userBkgImg']
            ext = image.name.split('.')[-1]
            imageUrl = default_storage.save(
                'image/userBkgImg/' + str(request.user.id) + '.' + ext, ContentFile(image.read()))
            profile.userBkgUrl = imageUrl

        profile.save()

        profileSerializer = serializers.ProfileSerializer(instance=profile)
        return Response(profileSerializer.data, status=status.HTTP_200_OK)


class FollowView(APIView):
    """
        Let User Follow Another User
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format='json'):
        if 'followUserId' not in request.data:
            return Response("No User Specified", status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        followedUserId = request.data['followUserId']
        followedUser = User.objects.get(pk=followedUserId)
        follow = models.Follow.objects.filter(
            user=user, followedUser=followedUser).first()

        if user == followedUser:
            return Response("Cannot Follow Self", status=status.HTTP_400_BAD_REQUEST)

        if follow is None:
            # has not been followed before
            followSerializer = serializers.FollowSerializer(
                data={"user": user.id, "followedUser": followedUser.id})
            if followSerializer.is_valid() and followSerializer.save():

                # create notification
                notificationSerializer = serializers.NotificationSerializer(
                    data={'user': followedUser.id, 'type': "follow", 'followUserId': request.user.id, 'followUserInfo': "@"+request.user.username})
                if notificationSerializer.is_valid():
                    notificationSerializer.save()

                return Response({"isFollowed": True})
            # else does nothing and falls to isFollow=False
        else:
            follow.delete()
        return Response({"isFollowed": False})


class FollowDetail(APIView):
    """
        Get all users that follow userId
    """

    def post(self, request, format='json'):
        # if userId == None, check the authentication user
        if 'userId' not in request.data:
            if request.user.is_authenticated:
                userId = request.user.id
            else:
                return Response("No User Specified", status=status.HTTP_400_BAD_REQUEST)
        else:
            userId = request.data['userId']

        user = User.objects.get(pk=userId)
        followingUsers = models.Follow.objects.filter(
            followedUser=user).values_list('user', flat=True)
        profiles = models.Profile.objects.filter(user__in=followingUsers)
        profileSerializer = serializers.ProfileSerializer(
            instance=profiles, many=True)

        return Response(profileSerializer.data)


class BlockView(APIView):
    """
        Let User Block Another User
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format='json'):
        if 'blockUserId' not in request.data:
            return Response("No User Specified", status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        blockedUserId = request.data['blockUserId']
        blockedUser = User.objects.get(pk=blockedUserId)
        block = models.Block.objects.filter(
            user=user, blockedUser=blockedUser).first()

        if user == blockedUser:
            return Response("Cannot Block Self", status=status.HTTP_400_BAD_REQUEST)

        if block is None:
            # has not been blocked before
            blockSerializer = serializers.BlockSerializer(
                data={"user": user.id, "blockedUser": blockedUser.id})
            if blockSerializer.is_valid() and blockSerializer.save():
                return Response({"isBlocked": True})
            # else does nothing and falls to isBlocked=False
        else:
            block.delete()
        return Response({"isBlocked": False})


class BlockDetail(APIView):
    """
        Get all user blocked
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        blockedUsers = models.Block.objects.filter(
            user=request.user).values_list('blockedUser', flat=True)
        profiles = models.Profile.objects.filter(user__in=blockedUsers)
        profileSerializer = serializers.ProfileSerializer(
            instance=profiles, many=True)

        return Response(profileSerializer.data)


class NotificationView(APIView):
    """
        Get Notifications for User
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        notifications = models.Notification.objects.filter(
            user=request.user.id).order_by('-createDate')

        notificationSerializer = serializers.NotificationSerializer(
            instance=notifications, many=True)

        response = notificationSerializer.data.copy()

        notifications.delete()

        return Response(response, status=status.HTTP_200_OK)
