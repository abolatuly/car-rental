import uuid
from typing import Protocol, OrderedDict
from django.db import transaction
from django.db.models import QuerySet, Q
from datetime import datetime, timedelta

from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import get_object_or_404

from . import models, choices
from users import models as user_models
from payments import choices as payment_choices
from payments import models as payment_models
from damage_detection import models as damage_detection_models


class OrderReposInterface(Protocol):

    @staticmethod
    def create_order(data: OrderedDict) -> tuple[models.Order, payment_models.Bill]:
        ...

    @staticmethod
    def get_orders(user: user_models.CustomUser) -> QuerySet[models.Order]:
        ...

    @staticmethod
    def complete_order(order_id: uuid.UUID, user: user_models.CustomUser) -> JsonResponse | None:
        ...

    @staticmethod
    def cancel_order(order_id: uuid.UUID, user: user_models.CustomUser) -> None:
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
    def get_orders(user: user_models.CustomUser) -> QuerySet[models.Order]:
        return models.Order.objects.filter(
            user=user
        )

    @staticmethod
    def complete_order(order_id: uuid.UUID, user: user_models.CustomUser) -> JsonResponse | None:
        order = get_object_or_404(
            models.Order.objects.filter(
                id=order_id,
                user=user,
                status=choices.OrderStatusChoices.Paid,
                order_item__pick_up_date__lte=timezone.now(),
            ))

        # check if all bills for the order have been paid
        bill_count = payment_models.Bill.objects.filter(order=order).count()
        paid_bill_count = payment_models.Bill.objects.filter(
            Q(order=order) & Q(status=payment_choices.BillStatusChoices.Paid)
        ).count()
        is_all_bills_paid = bill_count == paid_bill_count

        # check if the order has been processed by damage detection
        is_order_processed = damage_detection_models.DamageDetection.objects.filter(order=order).exists()

        if is_all_bills_paid and is_order_processed:
            order.status = choices.OrderStatusChoices.Delivered
            order.save()
        else:
            if not is_all_bills_paid:
                message = 'Order cannot be completed because not all bills have been paid.'
            else:
                message = 'Order cannot be completed because it has not been processed by damage detection.'

                # return an error response with the appropriate message
            return JsonResponse({'error': message}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def cancel_order(order_id: uuid.UUID, user: user_models.CustomUser) -> None:
        with transaction.atomic():
            order = get_object_or_404(
                models.Order.objects.filter(
                    Q(id=order_id),
                    Q(user=user),
                    Q(status=choices.OrderStatusChoices.Paid) | Q(status=choices.OrderStatusChoices.New),
                    Q(order_item__pick_up_date__gt=timezone.now())
                )
            )
            order.status = choices.OrderStatusChoices.Cancel
            order.save()

            bill = payment_models.Bill.objects.get(
                order=order
            )
            if order.status == choices.OrderStatusChoices.Paid:
                bill.status = payment_choices.BillStatusChoices.Refund
                bill.save()
            else:
                bill.status = payment_choices.BillStatusChoices.Expired
                bill.save()



