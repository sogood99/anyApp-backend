from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db.models import Q
from rest_framework.authtoken.models import Token
import datetime

from . import serializers, models
from accounts import models as accountModels, serializers as accountSerializers


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

        if 'repliesId' in request.data:
            repliesId = request.data['repliesId']
            try:
                repliesId = int(repliesId)
            except:
                repliesId = None
        else:
            repliesId = None

        if 'location' in request.data:
            location = request.data['location']
        else:
            location = None

        if 'image' in request.FILES:
            image = request.FILES['image']
            ext = image.name.split('.')[-1]
            imageUrl = default_storage.save(
                'image/tweet/' + str(tweet.id) + '.' + ext, ContentFile(image.read()))
        else:
            imageUrl = None

        if 'video' in request.FILES:
            video = request.FILES['video']
            ext = video.name.split('.')[-1]
            videoUrl = default_storage.save(
                'video/tweet/' + str(tweet.id) + '.' + ext, ContentFile(video.read()))
        else:
            videoUrl = None

        if 'audio' in request.FILES:
            audio = request.FILES['audio']
            ext = audio.name.split('.')[-1]
            audioUrl = default_storage.save(
                'audio/tweet/' + str(tweet.id) + '.' + ext, ContentFile(audio.read()))
        else:
            audioUrl = None

        tweet.text = text
        tweet.location = location
        tweet.imageUrl = imageUrl
        tweet.videoUrl = videoUrl
        tweet.audioUrl = audioUrl
        if repliesId is not None:
            tweet.repliesTweet = models.Tweet.objects.get(pk=repliesId)
        else:
            tweet.repliesTweet = None
        tweet.save()

        if repliesId is not None:
            # create notification for repliesId
            repliesTweet = models.Tweet.objects.get(pk=repliesId)
            repliedUser = repliesTweet.user
            notificationSerializer = accountSerializers.NotificationSerializer(
                data={'user': repliedUser.id, 'type': "reply", 'tweetId': repliesTweet.id, 'replyTweetId': tweet.id, 'replyTweetBrief': tweet.text})
            if notificationSerializer.is_valid():
                notificationSerializer.save()

        tweetSerializer = serializers.TweetSerializer(
            user=request.user, instance=tweet)
        return Response(tweetSerializer.data, status=status.HTTP_200_OK)


class DeleteTweet(APIView):
    """
        Let User Delete Tweet
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format='json'):
        if 'tweetId' not in request.data:
            return Response("Bad request", status=status.HTTP_400_BAD_REQUEST)
        tweet: models.Tweet = models.Tweet.objects.get(
            pk=request.data['tweetId'])
        if tweet.user == request.user:
            tweet.delete()
            return Response("Delete Success", status=status.HTTP_200_OK)
        return Response("Wrong user", status=status.HTTP_400_BAD_REQUEST)


class GetFeed(APIView):
    """
       Get Feed for user
    """

    def post(self, request, format='json'):
        def filterByBlocked(querySet):
            # given queryset, filter by excluding all blocked users
            if not request.user.is_authenticated:
                return querySet
            else:
                blockedUser = accountModels.Block.objects.filter(
                    user=request.user).values_list('blockedUser', flat=True)
                return querySet.filter(~Q(user__in=blockedUser))

        def recentFeed():
            # defaults to giving most recent
            tweets = models.Tweet.objects.order_by('-createDate')
            tweets = filterByBlocked(tweets)
            tweetSerializer = serializers.TweetSerializer(user=request.user,
                                                          instance=tweets, many=True)

            return Response(tweetSerializer.data)

        def popularFeed():
            # orders by popular
            tweets = models.Tweet.objects.all()
            tweets = filterByBlocked(tweets)
            tweetSerializer = serializers.TweetSerializer(user=request.user,
                                                          instance=tweets, many=True)
            ordered = sorted(tweetSerializer.data,
                             key=lambda t: (t['likes'], t['createDate']), reverse=True)

            return Response(ordered)

        def repliesFeed(tweetId):
            # feed of tweets
            targetTweet = models.Tweet.objects.get(pk=tweetId)

            tweets = models.Tweet.objects.filter(
                repliesTweet=targetTweet).order_by('-createDate').all()
            tweets = filterByBlocked(tweets)
            tweetSerializer = serializers.TweetSerializer(user=request.user,
                                                          instance=tweets, many=True)
            return Response(tweetSerializer.data)

        def profileFeed(user):
            # feed of profile of user authed
            tweets = models.Tweet.objects.filter(
                user=user).order_by('-createDate')
            tweets = filterByBlocked(tweets)
            tweetSerializer = serializers.TweetSerializer(user=request.user,
                                                          instance=tweets, many=True)
            return Response(tweetSerializer.data)

        def followingFeed(user):
            # following feed of user
            followingUsers = accountModels.Follow.objects.filter(
                user=user).values_list('followedUser', flat=True)

            tweets = models.Tweet.objects.filter(
                user__in=followingUsers).order_by('-createDate')
            tweets = filterByBlocked(tweets)
            tweetSerializer = serializers.TweetSerializer(
                user=user, instance=tweets, many=True)
            return Response(tweetSerializer.data)

        if 'option' not in request.data:
            return popularFeed()
        else:
            option = request.data['option']
            if option == "Recent":
                return recentFeed()
            elif option == "Popular":
                return popularFeed()
            elif option == "Following" and request.user.is_authenticated:
                return followingFeed(request.user)
            elif option == "Profile" and request.user.is_authenticated:
                return profileFeed(request.user)
            elif option == 'ProfileDetail' and 'userId' in request.data:
                user = User.objects.get(pk=request.data['userId'])
                return profileFeed(user)
            elif option == "Replies" and 'repliesId' in request.data:
                return repliesFeed(tweetId=request.data['repliesId'])
            else:
                return recentFeed()


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
            if likeSerializer.is_valid():
                like = likeSerializer.save()
                if like:

                    # create notification for repliesId
                    notificationSerializer = accountSerializers.NotificationSerializer(
                        data={'user': like.tweet.user.id, 'type': "like", 'tweetId': like.tweet.id, 'tweetBrief': like.tweet.text, 'likeUserId': like.user.id, 'likeUserInfo': "@"+like.user.username})
                    if notificationSerializer.is_valid():
                        notificationSerializer.save()

                    return Response({"isLike": True})
            # else does nothing and falls to isLike=False
        else:
            like.delete()
        return Response({"isLike": False})


class LikeDetail(APIView):
    """
        Get all users that liked a tweet
    """

    def post(self, request, format='json'):
        if 'tweet' not in request.data:
            return Response("No Tweet Specified", status=status.HTTP_400_BAD_REQUEST)

        tweetId = request.data['tweet']
        tweet = models.Tweet.objects.get(pk=tweetId)
        users = models.Like.objects.filter(
            tweet=tweet).values_list('user', flat=True)
        profiles = accountModels.Profile.objects.filter(user__in=users)
        profileSerializer = accountSerializers.ProfileSerializer(
            instance=profiles, many=True)

        return Response(profileSerializer.data)


class TweetDetail(APIView):

    """
        Let User access info about a single Tweet
    """

    def post(self, request, format='json'):
        if 'tweet' not in request.data:
            return Response("No Tweet Specified", status=status.HTTP_400_BAD_REQUEST)

        tweetId = request.data['tweet']
        tweet = models.Tweet.objects.get(pk=tweetId)
        tweetSerializer = serializers.TweetSerializer(
            user=request.user, instance=tweet)
        return Response(tweetSerializer.data)


class TweetSearch(APIView):

    """
        Search for tweets based on argument
    """

    def post(self, request, format='json'):
        if 'searchArg' not in request.data:
            return Response("Search Argument Unspecified", status=status.HTTP_400_BAD_REQUEST)

        import shlex
        import argparse

        parser = argparse.ArgumentParser(description="Search Argument")
        parser.add_argument('-s', '--string', nargs='*',
                            type=str, help='Search in string')
        parser.add_argument('-df', '--dateFrom', nargs='?', help="df <=",
                            type=datetime.date.fromisoformat)
        parser.add_argument('-dt', '--dateTo', nargs='?', help="<= dt",
                            type=datetime.date.fromisoformat)
        parser.add_argument('-to', '--textOnly',
                            action='store_true', help="Contains only text")
        parser.add_argument(
            '-i', '--image', action='store_true', help="Contains Image")
        parser.add_argument(
            '-v', '--video', action='store_true', help="Contains Video")

        searchArg = request.data['searchArg']
        args = parser.parse_args(shlex.split(searchArg))

        queryset = models.Tweet.objects
        if args.textOnly == True:
            queryset = queryset.filter((Q(imageUrl=None) & Q(videoUrl=None)))

        if args.image == True:
            queryset = queryset.filter(~Q(imageUrl=None))

        if args.video:
            queryset = queryset.filter(~Q(videoUrl=None))

        if args.dateTo:
            queryset = queryset.filter(createDate__date__lte=args.dateTo)

        if args.dateFrom:
            queryset = queryset.filter(createDate__date__gte=args.dateFrom)

        # for checking profile related fuzzy search in backend
        newQ = accountModels.Profile.objects.filter(
            user__in=queryset.values_list('user', flat=True))

        if args.string is not None:
            # filter by username
            usernameQ = Q()
            argsStringNoUsername = args.string.copy()
            for s in args.string:
                if (s[0] == '@'):
                    usernameQ = usernameQ | Q(user__username=s[1:])
                    argsStringNoUsername.remove(s)

            queryset = queryset.filter(usernameQ)

            # filter by search terms
            q = Q()
            for s in argsStringNoUsername:
                q = q | Q(text__contains=s)
                q = q | Q(user__username__contains=s)
                tempQ = newQ.filter(profileName__contains=s)
                q = q | Q(user__in=tempQ.values_list('user', flat=True))
            queryset = queryset.filter(q)

        tweetSerializer = serializers.TweetSerializer(
            user=request.user, instance=queryset, many=True)
        return Response(tweetSerializer.data)
