from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

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
                profile_json = {'user': user.id, 'profile_name': 'New Profile'}
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


class ProfileJson(APIView):
    """
        Get Profile Information
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = models.Profile.objects.get(pk=request.user)
        if profile:
            profile_serializer = serializers.ProfileSerializer(
                instance=profile)
            return Response(profile_serializer.data)
        return Response('Failed', status=status.HTTP_400_BAD_REQUEST)
