from rest_framework import serializers
from django.contrib.auth.models import UsersProfile
from .models import *


class UserSer(serializers.ModelSerializer):
    """Сериализация пользователя"""
    class Meta:
        model = User
        fields = ("username", "email")


class ProfileSer(serializers.ModelSerializer):
    """Профиль пользователя"""
    user = UserSer()

    class Meta:
        model = UsersProfile
        fields = ("user", "avatar", "university", "about")


class ProfileUpdateSer(serializers.ModelSerializer):
    """Редактирование профиля пользователя"""
    class Meta:
        model = UsersProfile
        fields = ("user", "avatar", "university", "about")


class AvatarUpdateSer(serializers.ModelSerializer):
    """Редактирование аватар ользователя"""
    class Meta:
        model = UsersProfile
        fields = ("avatar")