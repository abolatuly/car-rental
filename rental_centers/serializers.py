from rest_framework import serializers
from cars import serializers as cars_serializers
from . import models


class CreateRentalCenterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RentalCenter
        fields = '__all__'


class RentalCenterSerializer(serializers.ModelSerializer):
    cars = cars_serializers.CarSerializer(many=True)

    class Meta:
        model = models.RentalCenter
        fields = '__all__'
