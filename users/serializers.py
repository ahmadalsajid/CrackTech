from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
)
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from icecream import ic
from .models import User


class LoginViewSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["token"] = {
            "refresh": data.pop("refresh"),
            "access": data.pop("access"),
        }
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

