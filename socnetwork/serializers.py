from rest_framework import serializers
from django.contrib.auth.models import UsersProfile
from .models import *


class UserSer(serializers.ModelSerializer):
    """Серіалізація користувача"""
    class Meta:
        model = User
        fields = ("username", "email")


class ProfileSer(serializers.ModelSerializer):
    """Профіль користувача"""
    user = UserSer()

    class Meta:
        model = UsersProfile
        fields = ("user", "avatar", "university", "about")


class ProfileUpdateSer(serializers.ModelSerializer):
    """Редагування профіля користувача"""
    class Meta:
        model = UsersProfile
        fields = ("user", "avatar", "university", "about")


class AvatarUpdateSer(serializers.ModelSerializer):
    """Редагування аватару користувача"""
    class Meta:
        model = UsersProfile
        fields = ("avatar")