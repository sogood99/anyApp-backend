
from django.urls import path, re_path
from rest_framework.authtoken import views as auth_views

from . import views

urlpatterns = [
    path('like/', views.LikeView.as_view(), name='like'),
    path('feed/', views.GetFeed.as_view(), name='feed'),
    path('detail/', views.TweetDetail.as_view(), name='tweet-detail'),
    path('', views.SendTweet.as_view(), name='tweet'),
]
