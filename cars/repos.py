from typing import Protocol
from django.db.models import QuerySet
from . import models


class CarReposInterface(Protocol):

    @staticmethod
    def get_cars() -> QuerySet[models.Car]:
        ...


class CarReposV1:

    @staticmethod
    def get_cars() -> QuerySet[models.Car]:
        return models.Car.objects.all()
