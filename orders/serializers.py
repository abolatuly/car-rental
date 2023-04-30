from rest_framework import serializers
from . import models


class _CreateOrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OrderItem
        fields = (
            'car',
            'pick_up_location',
            'drop_off_location',
            'pick_up_date',
            'drop_off_date'
        )


class CreateOrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_item = _CreateOrderItemSerializer(write_only=True, many=True)

    class Meta:
        model = models.Order
        fields = ('order_item', 'user')


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer()

    class Meta:
        model = models.Order
        fields = ('status', 'user', 'number', 'order_item')
