import uuid
from typing import Protocol, OrderedDict

from . import repos, models
from users import models as user_models


class DamageDetectionServicesInterface(Protocol):

    def damage_detection(self, data: OrderedDict, user: user_models.CustomUser) -> models.DamageDetection:
        ...

    def get_detections(self, order_id: uuid.UUID) -> models.DamageDetection | None:
        ...


class DamageDetectionServicesV1:
    damage_detection_repos: repos.DamageDetectionReposInterface = repos.DamageDetectionReposV1()

    def damage_detection(self, data: OrderedDict, user: user_models.CustomUser) -> models.DamageDetection:
        return self.damage_detection_repos.damage_detection(data=data, user=user)

    def get_detections(self, order_id: uuid.UUID) -> models.DamageDetection | None:
        return self.damage_detection_repos.get_detections(order_id=order_id)
