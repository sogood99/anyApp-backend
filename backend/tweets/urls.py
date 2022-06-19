
from django.urls import path
from rest_framework.authtoken import views as auth_views

from . import views

urlpatterns = [
    path('like/', views.LikeView.as_view(), name='like'),
    path('like/detail/', views.LikeDetail.as_view(), name='like-detail'),
    path('feed/', views.GetFeed.as_view(), name='feed'),
    path('detail/', views.TweetDetail.as_view(), name='tweet-detail'),
    path('search/', views.TweetSearch.as_view(), name='tweet-search'),
    path('', views.SendTweet.as_view(), name='tweet'),
]
