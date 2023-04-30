from rest_framework import serializers
from . import models


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'date_of_birth')


class VerifyUserSerializer(serializers.Serializer):
    session_id = serializers.UUIDField()
    code = serializers.CharField(max_length=4)


class CreateTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()