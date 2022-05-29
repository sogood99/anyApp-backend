from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.authtoken.models import Token

from . import serializers, models


class Tweet(APIView):
    """
        Let User Access/Create Tweets
    """

    def post(self, request, format='json'):
        data = request.FILES['image']
        path = default_storage.save(
            'image/test.jpg', ContentFile(data.read()))

        return Response("Yass", status=status.HTTP_200_OK)


class Like(APIView):
    """
        Let User Like a Tweet
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format='json'):
        return Response("Hello")
