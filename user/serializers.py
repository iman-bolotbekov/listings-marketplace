from typing import Dict, Any

from django.contrib.auth import get_user_model

from djoser.serializers import UserCreateSerializer

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'isAdmin')

    def get_isAdmin(self, obj):
        return obj.is_staff


class UserSerializer(serializers.ModelSerializer):
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'isAdmin')

    def get_isAdmin(self, obj):
        return obj.is_staff
