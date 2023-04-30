import uuid
import logging
from celery import shared_task
from payments import models, choices


logger = logging.getLogger(__name__)


@shared_task()
def check_bill_expires_at(bill_id: uuid.UUID) -> None:
    try:
        bill = models.Bill.objects.get(
            id=bill_id,
            status=choices.BillStatusChoices.New,
        )
        bill.status = choices.BillStatusChoices.Expired
        bill.save()
        logger.info(f'Bill with id {bill_id} set status "EXPIRED"')
    except models.Bill.DoesNotExist:
        logger.error(f'Bill with id {bill_id} not found')

