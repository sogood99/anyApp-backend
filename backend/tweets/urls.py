
from django.urls import path, re_path
from rest_framework.authtoken import views as auth_views

from . import views

urlpatterns = [
    path('', views.Tweet.as_view(), name='tweet'),
]
