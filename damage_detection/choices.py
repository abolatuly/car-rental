from django.db import models


class DamageStatusChoices(models.TextChoices):
    NoDamage = 'No Damage'
    Damaged = 'Damaged'
