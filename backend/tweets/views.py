from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.authtoken.models import Token

from . import serializers, models


class SendTweet(APIView):
    """
        Let User Access/Create Tweets
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format='json'):

        tweet = models.Tweet.objects.create(user=request.user)

        if 'text' in request.data:
            text = request.data['text']
        else:
            text = None
        if 'image' in request.FILES:
            image = request.FILES['image']
            ext = image.name.split('.')[-1]
            imageUrl = default_storage.save(
                'image/tweet/' + str(tweet.id) + '.' + ext, ContentFile(image.read()))
        else:
            imageUrl = None

        tweet.text = text
        tweet.imageUrl = imageUrl
        tweet.save()

        tweetSerializer = serializers.TweetSerializer(instance=tweet)

        return Response(tweetSerializer.data, status=status.HTTP_200_OK)


class GetFeed(APIView):
    """
       Get Feed for user 
    """

    def get(self, request):
        tweets = models.Tweet.objects.all()[:10]
        tweetSerializer = serializers.TweetSerializer(
            instance=tweets, many=True)
        return Response(tweetSerializer.data)


class Like(APIView):
    """
        Let User Like a Tweet
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format='json'):
        return Response("Hello")
