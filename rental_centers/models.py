from django.db import models
from django.utils.translation import gettext_lazy as _
from . import choices


class RentalCenter(models.Model):
    cars = models.ManyToManyField(
        to='cars.Car',
        related_name='rental_centers'
    )
    location = models.CharField(max_length=15, choices=choices.LocationChoices.choices,
                                verbose_name=_('Location'), unique=True)
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active?'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Rental Center')
        verbose_name_plural = _('Rental Centers')
