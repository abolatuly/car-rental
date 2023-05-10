from rest_framework import serializers

from . import models


class CreateDamageDetectionSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(format='hex_verbose')

    class Meta:
        model = models.DamageDetection
        fields = ('order_id', 'front_image', 'left_image', 'right_image', 'back_image')


class DamageDetectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DamageDetection
        fields = ('order', 'status', 'data')
