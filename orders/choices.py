from django.db import models


class OrderStatusChoices(models.TextChoices):
    New = 'New'
    ProcessInProgress = 'ProcessInProgress'
    Damaged = 'Damaged'
    Cancel = 'Cancel'
    Paid = 'Paid'
    Overuse = 'Overuse'
    Delivered = 'Delivered'
