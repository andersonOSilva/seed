from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer de usuário.
    """
    class Meta:
        model = User
        depth = 1
        fields = [
            'email',
            'password'
        ]


class UserListSerializer(serializers.ModelSerializer):
    """
    Serializador de usuário (sem senha).
    """
    class Meta:
        model = User
        depth = 1
        fields = [
            'email'
        ]
