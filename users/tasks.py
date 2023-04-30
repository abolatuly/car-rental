import logging

from celery import shared_task
from templated_email import send_templated_mail

from src import settings

logger = logging.getLogger(__name__)


@shared_task()
def send_welcome_letter(user_info: dict) -> None:
    try:
        send_templated_mail(
            template_name='welcome',  # name of the file in templated_email
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_info['user_email']],
            context={
                'first_name': user_info['user_first_name'],
            },
            bcc=[user_info['user_email']],
        )
        logger.info(f'Welcome email for the user {user_info["user_first_name"]} has been SENT')
    except Exception as e:
        logger.info(f'Welcome email for the user {user_info["user_first_name"]} has NOT been SENT. Because {e}')


@shared_task()
def send_code_to_email(email: str, code: str) -> None:
    try:
        send_templated_mail(
            template_name='code',  # name of the file in templated_email
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            context={
                'code': code
            },
            bcc=[email],
        )
        logger.info(f'Email with code for the user {email} has been SENT')
    except Exception as e:
        logger.info(f'Email with code for the user {email} has NOT been SENT. Because {e}')

