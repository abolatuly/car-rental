from django.db import models


class BillStatusChoices(models.TextChoices):
    New = 'New'
    Pending = 'Pending'
    Paid = 'Paid'
    Expired = 'Expired'
    Refund = 'Refund'
    RefundPartially = 'Refund Partially'


class TransactionTypeChoices(models.TextChoices):
    Charge = 'Charge'
    Refund = 'Refund'
