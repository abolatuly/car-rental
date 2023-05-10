from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from . import serializers, services, models
from mixins import mixins


class DamageDetectionViewSet(mixins.ActionSerializerMixin, ModelViewSet):
    ACTION_SERIALIZERS = {
        'create': serializers.CreateDamageDetectionSerializer,
    }
    damage_detection_services: services.DamageDetectionServicesInterface = services.DamageDetectionServicesV1()
    serializer_class = serializers.DamageDetectionSerializer
    queryset = models.DamageDetection.objects.all()
    permission_classes = permissions.IsAuthenticated,

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        car_damage = self.damage_detection_services.damage_detection(data=serializer.validated_data, user=request.user)

        data = serializers.DamageDetectionSerializer(car_damage).data
        return Response(data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        detection = self.damage_detection_services.get_detections(order_id=self.kwargs['order_id'])

        if detection:
            data = serializers.DamageDetectionSerializer(detection).data
            return Response(data)
        return Response(status=status.HTTP_404_NOT_FOUND)

