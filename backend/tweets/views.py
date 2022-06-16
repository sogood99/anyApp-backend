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

        tweetSerializer = serializers.TweetSerializer(
            user=request.user, instance=tweet)
        return Response(tweetSerializer.data, status=status.HTTP_200_OK)


class GetFeed(APIView):
    """
       Get Feed for user 
    """

    def post(self, request, format='json'):
        def popularFeed():
            # defaults to giving most recent
            tweets = models.Tweet.objects.order_by('-createDate').all()
            tweetSerializer = serializers.TweetSerializer(user=request.user,
                                                          instance=tweets, many=True)
            return Response(tweetSerializer.data)

        def profileFeed(user):
            # feed of tweets sent by user
            tweets = models.Tweet.objects.filter(
                user=user).order_by('-createDate').all()
            tweetSerializer = serializers.TweetSerializer(user=request.user,
                                                          instance=tweets, many=True)
            return Response(tweetSerializer.data)

        if 'option' not in request.data:
            return popularFeed()
        else:
            option = request.data['option']
            if option == "Popular":
                return popularFeed()
            elif option == "Profile" and request.user.is_authenticated:
                return profileFeed(request.user)
            else:
                return popularFeed()


class LikeView(APIView):
    """
        Let User Like a Tweet
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format='json'):
        if 'tweet' not in request.data:
            return Response("No Tweet Specified", status=status.HTTP_400_BAD_REQUEST)

        userId = request.user.id
        tweetId = request.data['tweet']
        like = models.Like.objects.filter(
            user=request.user, tweet=tweetId).first()
        if like is None:
            # has not been liked before
            likeSerializer = serializers.LikeSerializer(
                data={"user": userId, "tweet": tweetId})
            if likeSerializer.is_valid() and likeSerializer.save():
                return Response({"isLike": True})
            # else does nothing and falls to isLike=False
        else:
            like.delete()
        return Response({"isLike": False})
