from rest_framework import status, permissions
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
