from rest_framework.viewsets import ModelViewSet
from . import serializers, permissions, services
from utils import mixins


class CarViewSet(mixins.ActionSerializerMixin, ModelViewSet):
    ACTION_SERIALIZERS = {
        'retrieve': serializers.RetrieveCarSerializer,
    }
    car_services: services.CarServicesInterface = services.CarServicesV1()
    serializer_class = serializers.CarSerializer
    queryset = car_services.get_cars()
    permission_classes = permissions.IsAdminOrReadOnly,
