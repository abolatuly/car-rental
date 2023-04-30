from django.db import models


class LocationChoices(models.TextChoices):
    Almaty = 'Almaty'
    Astana = 'Astana'
    Shymkent = 'Shymkent'
    Karaganda = 'Karaganda'
    Taraz = 'Taraz'
    Aqtobe = 'Aqtobe'
