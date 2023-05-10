import uuid
from typing import Protocol, OrderedDict
from django.db.models import QuerySet
from django.http import JsonResponse

from . import models, repos
from users import models as user_models
from payments import tasks as payment_tasks


class OrderServicesInterface(Protocol):

    def create_order(self, data: OrderedDict) -> models.Order:
        ...

    def get_orders(self, user: user_models.CustomUser) -> QuerySet[models.Order]:
        ...

    def complete_order(self, order_id: uuid.UUID, user: user_models.CustomUser) -> JsonResponse | None:
        ...

    def cancel_order(self, order_id: uuid.UUID, user: user_models.CustomUser) -> None:
        ...


class OrderServicesV1:
    order_repos: repos.OrderReposInterface = repos.OrderReposV1()

    def create_order(self, data: OrderedDict) -> models.Order:
        order, bill = self.order_repos.create_order(data=data)
        payment_tasks.check_bill_expires_at.apply_async(
            (bill.id,),
            eta=bill.expires_at,
        )

        return order

    def get_orders(self, user: user_models.CustomUser) -> QuerySet[models.Order]:
        return self.order_repos.get_orders(user=user)

    def complete_order(self, order_id: uuid.UUID, user: user_models.CustomUser) -> JsonResponse | None:
        return self.order_repos.complete_order(order_id=order_id, user=user)

    def cancel_order(self, order_id: uuid.UUID, user: user_models.CustomUser) -> None:
        self.order_repos.cancel_order(order_id=order_id, user=user)
