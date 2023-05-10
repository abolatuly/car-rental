import random
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from orders import choices


class Order(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.PROTECT,
        related_name='orders'
    )

    number = models.CharField(max_length=10, unique=True)

    status = models.CharField(
        max_length=20,
        choices=choices.OrderStatusChoices.choices,
        default=choices.OrderStatusChoices.New,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def generate_number(cls) -> str:
        number = ''.join(random.choices('0123456789', k=10))

        if cls.objects.filter(number=number).exists():
            return cls.generate_number()

        return number

    class Meta:
        ordering = ('-created_at',)


class OrderItem(models.Model):
    order = models.OneToOneField(to=Order, on_delete=models.PROTECT, related_name='order_item')
    car = models.ForeignKey(
        to='cars.Car',
        on_delete=models.PROTECT,
        related_name='order_item',
        limit_choices_to={'is_active': True},
    )
    pick_up_location = models.ForeignKey(
        to='rental_centers.RentalCenter',
        on_delete=models.PROTECT,
        related_name='pick_up_location',
        verbose_name=_('Pick-up location')
    )
    drop_off_location = models.ForeignKey(
        to='rental_centers.RentalCenter',
        on_delete=models.PROTECT,
        related_name='drop_off_location',
        verbose_name=_('Drop-off location')
    )
    pick_up_date = models.DateField(verbose_name=_("Pick-up date"))
    drop_off_date = models.DateField(verbose_name=_("Drop-off date"))
    amount = models.DecimalField(max_digits=14, decimal_places=2)
