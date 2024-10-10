from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
)
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from icecream import ic

from .models import Student, User


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


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'first_name', 'last_name',
            'phone', 'is_verified', 'is_deleted'
        ]
        extra_kwargs = {
            'username': {'validators': [UnicodeUsernameValidator()]},
        }
        # fields = '__all__'
        # exclude = ['last_login', 'is_superuser', 'is_staff', 'date_joined', 'groups', 'user_permissions']


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ['password', ]


class StudentCreateSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.pop('user')
        user = User.objects.create(**user)
        student = Student.objects.create(user=user, **validated_data)
        return student

    def update(self, instance, validated_data):
        try:
            user_data = validated_data.pop('user') if 'user' in validated_data else None
            if user_data:
                User.objects.filter(username=user_data['username']).update(**user_data)
            instance = super().update(instance, validated_data)
            user = User.objects.filter(username=user_data['username']).first()
            instance.user = user
            instance.save()
            return instance
        except Exception as e:
            ic(e)


class StudentSerializer(serializers.ModelSerializer):
    user = UserRetrieveSerializer()

    class Meta:
        model = Student
        fields = '__all__'
