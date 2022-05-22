from dataclasses import field
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(required=False,
                                     validators=[UniqueValidator(
                                         queryset=User.objects.all())],
                                     max_length=32)
    password = serializers.CharField(required=True,
                                     min_length=6,
                                     write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    profile_name = serializers.CharField(max_length=20)

    class Meta:
        model = Profile
        fields = ('user', 'profile_name')
