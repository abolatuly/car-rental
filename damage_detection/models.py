import os
import uuid

from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from . import choices


def car_image_path(instance, filename):
    return os.path.join(f'car_damage_detection/{instance.order.user}',
                        f'{timezone.now().strftime("%Y-%m-%d")}_{filename}')


class DamageDetection(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    order = models.OneToOneField(
        to='orders.Order',
        on_delete=models.SET_NULL,
        null=True,
        related_name='damage_detection'
    )
    front_image = models.ImageField(
        upload_to=car_image_path,
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        verbose_name=_('Front Image')
    )
    left_image = models.ImageField(
        upload_to=car_image_path,
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        verbose_name=_('Left Image')
    )
    right_image = models.ImageField(
        upload_to=car_image_path,
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        verbose_name=_('Right Image')
    )
    back_image = models.ImageField(
        upload_to=car_image_path,
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],
        verbose_name=_('Back Image')
    )
    status = models.CharField(
        choices=choices.DamageStatusChoices.choices,
        max_length=9,
        blank=True,
        null=True
    )
    data = models.JSONField(
        default=dict,
        verbose_name=_('Data'),
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Damage Detection')
        verbose_name_plural = _('Damage Detections')
