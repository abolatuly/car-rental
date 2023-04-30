from rest_framework import serializers
from . import models


class CarSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = models.Car
        fields = '__all__'


class RetrieveCarSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = models.Car
        fields = '__all__'
