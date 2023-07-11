from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from . import models, pagination, serializers, services
from mixins import mixins


class OrderItemViewSet(ModelViewSet):
    serializer_class = serializers.OrderItemSerializer
    queryset = models.OrderItem.objects.all()


class OrderViewSet(mixins.ActionSerializerMixin, ModelViewSet):
    ACTION_SERIALIZERS = {
        'create': serializers.CreateOrderSerializer,
    }
    order_services: services.OrderServicesInterface = services.OrderServicesV1()
    serializer_class = serializers.OrderSerializer
    pagination_class = pagination.CustomPageNumberPagination
    permission_classes = permissions.IsAuthenticated,

    def get_queryset(self):
        return self.order_services.get_orders(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = self.order_services.create_order(data=serializer.validated_data)

        data = serializers.OrderSerializer(order).data
        return Response(data, status=status.HTTP_201_CREATED)

    def complete_order(self, request, *args, **kwargs):
        data = self.order_services.complete_order(order_id=kwargs['order_id'], user=request.user)
        if data:
            return data

        return Response(status=status.HTTP_200_OK)

    def cancel_order(self, request, *args, **kwargs):
        self.order_services.cancel_order(order_id=kwargs['order_id'], user=request.user)

        return Response(status=status.HTTP_200_OK)
