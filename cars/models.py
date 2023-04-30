import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class Car(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=100, verbose_name=_('Name'), unique=True)
    main_image = models.ImageField(upload_to='cars/', verbose_name=_('Main Image'))
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active?'))
    data = models.JSONField(default=dict, verbose_name=_('Data'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Car')
        verbose_name_plural = _('Cars')
