from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models, tasks


@receiver(post_save, sender=models.CustomUser)
def send_welcome_letter(sender, instance: models.CustomUser, **kwargs):
    if kwargs.get('created', False):
        user_info = {
            'user_email': instance.email,
            'user_first_name': instance.first_name
        }
        tasks.send_welcome_letter.delay(user_info=user_info)