import logging
from datetime import datetime

from celery import shared_task
from templated_email import send_templated_mail

from src import settings

logger = logging.getLogger(__name__)


@shared_task()
def send_order_email(order_item_info: dict) -> None:
    try:
        user_email = order_item_info.pop('user_email')
        order_item_info['pick_up_date'] = datetime.strptime(order_item_info['pick_up_date'],
                                                            '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d')
        order_item_info['drop_off_date'] = datetime.strptime(order_item_info['drop_off_date'],
                                                             '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d')
        send_templated_mail(
            template_name='order',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email],
            context=order_item_info,
            bcc=[user_email]
        )
        logger.info(f'Email for the order {order_item_info["order_number"]} has been SENT')
    except Exception as e:
        logger.error(f'Email for the order {order_item_info["order_number"]} has NOT been SENT. Because {e}')
