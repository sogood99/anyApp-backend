from django.urls import path
from rest_framework import authtoken

from . import views

urlpatterns = [
    path('create/', views.UserCreate.as_view(), name='account-create'),
]
