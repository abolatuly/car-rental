from typing import Protocol
from django.db.models import QuerySet
from . import models, repos


class CarServicesInterface(Protocol):

    def get_cars(self) -> QuerySet[models.Car]:
        ...


class CarServicesV1:
    car_repos: repos.CarReposInterface = repos.CarReposV1()

    def get_cars(self) -> QuerySet[models.Car]:
        return self.car_repos.get_cars()
