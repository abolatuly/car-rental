import random
import uuid

from django.db import models
from payments import choices


class Bill(models.Model):
    id = models.UUIDField(primary_key=True, editable=True, default=uuid.uuid4)
    order = models.ForeignKey(
        to='orders.Order',
        on_delete=models.SET_NULL,
        null=True,
        related_name='bill',
    )
    total = models.DecimalField(max_digits=14, decimal_places=2)
    number = models.CharField(max_length=10, unique=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        choices=choices.BillStatusChoices.choices,
        default=choices.BillStatusChoices.New,
        max_length=16,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def generate_number(cls) -> str:
        number = ''.join(random.choices('0123456789', k=10))

        if cls.objects.filter(number=number).exists():
            return cls.generate_number()

        return number


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, editable=True, default=uuid.uuid4)
    bill = models.ForeignKey(
        to=Bill,
        on_delete=models.SET_NULL,
        null=True,
        related_name='transactions',
    )
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    transaction_type = models.CharField(
        choices=choices.TransactionTypeChoices.choices,
        max_length=6,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
