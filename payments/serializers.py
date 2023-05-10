from rest_framework import serializers

from . import models


class BillSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Bill
        fields = '__all__'
