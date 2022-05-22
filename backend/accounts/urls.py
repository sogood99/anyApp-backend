from django.urls import path, re_path
from rest_framework.authtoken import views as auth_views

from . import views

urlpatterns = [
    re_path(r'^create/?$', views.UserCreate.as_view(), name='account-create'),
    re_path(r'^login/?$', auth_views.obtain_auth_token, name='login'),
    re_path(r'^profile/?$', views.ProfileJson.as_view(), name='profile-json'),
]
