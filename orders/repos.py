from typing import Protocol, OrderedDict
from django.db import transaction
from django.db.models import QuerySet
from datetime import datetime, timedelta
from django.utils import timezone

from . import models
from payments import models as payment_models


class OrderReposInterface(Protocol):

    @staticmethod
    def create_order(data: OrderedDict) -> tuple[models.Order, payment_models.Bill]:
        ...

    @staticmethod
    def get_orders() -> QuerySet[models.Order]:
        ...


class OrderReposV1:

    @staticmethod
    def create_order(data: OrderedDict) -> tuple[models.Order, payment_models.Bill]:
        with transaction.atomic():
            order_item = data.pop('order_item')
            order = models.Order.objects.create(
                number=models.Order.generate_number(),
                **data
            )

            pick_up_date = datetime.strptime(str(order_item[0]['pick_up_date']), '%Y-%m-%d').date()
            drop_off_date = datetime.strptime(str(order_item[0]['drop_off_date']), '%Y-%m-%d').date()
            num_days = (drop_off_date - pick_up_date).days

            models.OrderItem.objects.create(
                order=order,
                car=order_item[0]['car'],
                pick_up_location=order_item[0]['pick_up_location'],
                drop_off_location=order_item[0]['drop_off_location'],
                pick_up_date=order_item[0]['pick_up_date'],
                drop_off_date=order_item[0]['drop_off_date'],
                amount=num_days * order_item[0]['car'].amount
            )

            bill = payment_models.Bill.objects.create(
                order=order,
                total=order.order_item.amount,
                number=payment_models.Bill.generate_number(),
                expires_at=timezone.now() + timedelta(minutes=15)
            )

        return order, bill

    @staticmethod
    def get_orders() -> QuerySet[models.Order]:
        return models.Order.objects.all()