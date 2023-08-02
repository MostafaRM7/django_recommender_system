from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'password']

        password = serializers.CharField(write_only=True)