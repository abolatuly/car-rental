from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models, tasks


@receiver(post_save, sender=models.Order)
def send_order_notification(sender, instance: models.Order, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(instance.id),
        {
            'type': 'send_notification',
            'status': instance.status,
        }
    )


@receiver(post_save, sender=models.OrderItem)
def send_order_email(sender, instance: models.OrderItem, **kwargs):

    # Schedule feedback email task only for new orders
    if kwargs.get('created', False):
        order_item_info = {
            'user_email': instance.order.user.email,
            'order_number': instance.order.number,
            'car': instance.car.name,
            'pick_up_date': instance.pick_up_date,
            'drop_off_date': instance.drop_off_date,
            'pick_up_location': instance.pick_up_location.location,
            'drop_off_location': instance.drop_off_location.location,
        }
        tasks.send_order_email.delay(order_item_info=order_item_info)
