from rest_framework.viewsets import ModelViewSet
from mixins import mixins
from . import serializers, models, permissions


class RentalCenterViewSet(mixins.ActionSerializerMixin, ModelViewSet):
    ACTION_SERIALIZERS = {
        'create': serializers.CreateRentalCenterSerializer,
    }
    serializer_class = serializers.RentalCenterSerializer
    queryset = models.RentalCenter.objects.prefetch_related('cars')
