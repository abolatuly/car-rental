import uuid
import logging
from typing import Protocol
from django.db import transaction
from django.db.models import QuerySet
from rest_framework.generics import get_object_or_404

from payments import models, choices
from orders import models as order_models
from orders import choices as orders_choices


logger = logging.getLogger(__name__)


class BillReposInterface(Protocol):

    @staticmethod
    def pay_bill(order_id: uuid.UUID) -> None:
        ...

    @staticmethod
    def get_bill(order_id: uuid.UUID) -> models.Bill:
        ...


class BillReposV1:

    @staticmethod
    def pay_bill(order_id: uuid.UUID) -> None:
        with transaction.atomic():
            try:
                bill = BillReposV1.get_bill(order_id=order_id)
                bill.status = choices.BillStatusChoices.Paid
                bill.save()
                bill.order.status = orders_choices.OrderStatusChoices.Paid
                bill.order.save()

                models.Transaction.objects.create(
                    bill=bill,
                    amount=bill.total,
                    transaction_type=choices.TransactionTypeChoices.Charge,
                )
                logger.info(f'bill with id {order_id} is successfully paid!')
            except models.Bill.DoesNotExist:
                logger.error(f'bill with id {order_id} not found')

    @staticmethod
    def get_bill(order_id: uuid.UUID) -> models.Bill:
        bill = get_object_or_404(
            models.Bill.objects.filter(
                order=order_id,
                status=choices.BillStatusChoices.New,
            ),
        )
        return bill
