import io
import os
import uuid

import torch
from typing import Protocol, OrderedDict

from PIL import Image
from django.db import transaction, IntegrityError
from django.utils import timezone
from rest_framework.generics import get_object_or_404
from decimal import Decimal

from orders import models as order_models
from orders import choices as order_choices
from payments import models as payment_models
from users import models as user_models
from . import models, choices


class DamageDetectionReposInterface(Protocol):

    @staticmethod
    def damage_detection(data: OrderedDict, user: user_models.CustomUser) -> models.DamageDetection:
        ...

    @staticmethod
    def get_detections(order_id: uuid.UUID) -> models.DamageDetection | None:
        ...


class DamageDetectionReposV1:

    @staticmethod
    def damage_detection(data: OrderedDict, user: user_models.CustomUser) -> models.DamageDetection:
        with transaction.atomic():
            order_id = data.get('order_id')
            order = get_object_or_404(
                order_models.Order.objects.filter(
                    id=order_id,
                    user=user,
                    status=order_choices.OrderStatusChoices.Paid
                )
            )
            left_image = data.get('left_image')
            right_image = data.get('right_image')
            front_image = data.get('front_image')
            back_image = data.get('back_image')

            # Damage Detection feature
            damage_found = DamageDetectionReposV1._check_damage([left_image, right_image, front_image, back_image])

            # Fine fee calculation for the overuse time
            overuse = (timezone.now().date() - order.order_item.drop_off_date).days

            status = None
            total_fine_fee = 0

            if overuse > 0:
                overuse_fee = order.order_item.car.amount * Decimal(1.2) * overuse
                total_fine_fee += overuse_fee
                order.status = order_choices.OrderStatusChoices.Overuse
                order.save()

            if damage_found:
                status = choices.DamageStatusChoices.Damaged
                total_fine_fee += DamageDetectionReposV1._count_fine_fee(damage_found)
                order.status = order_choices.OrderStatusChoices.Damaged
                order.save()

            if total_fine_fee:
                payment_models.Bill.objects.create(
                    order=order,
                    total=total_fine_fee,
                    number=payment_models.Bill.generate_number()
                )

            try:
                car_damage = models.DamageDetection.objects.create(
                    order=order,
                    left_image=left_image,
                    right_image=right_image,
                    front_image=front_image,
                    back_image=back_image,
                    status=status or choices.DamageStatusChoices.NoDamage,
                    data=damage_found
                )

                return car_damage
            except IntegrityError:
                raise ValueError('Damage detection has already been processed for this order')

    @staticmethod
    def get_detections(order_id: uuid.UUID) -> models.DamageDetection | None:
        try:
            detection = models.DamageDetection.objects.get(order__id=order_id)
        except models.DamageDetection.DoesNotExist:
            return None
        else:
            return detection

    @classmethod
    def _check_damage(cls, images) -> dict:
        path_weightfile = os.path.join('static/', 'model/yolov5s.pt')
        model = torch.hub.load('ultralytics/yolov5', 'custom', path_weightfile)
        model.eval()
        damage_found = {}

        for image in images:
            image_bytes = image.read()
            img = Image.open(io.BytesIO(image_bytes))
            results = model(img)
            labels = [i.strip() for i in results.pandas().xyxy[0]['name']]

            for damage_type in labels:
                damage_found[damage_type] = 1 + damage_found.get(damage_type, 0)

        return damage_found

    @classmethod
    def _count_fine_fee(cls, damage_found: dict):
        # Fine fee for each damage category
        fine_fee_broken = 100
        fine_fee_deformation = 50
        fine_fee_broken_glass = 200
        fine_fee_scratch = 20

        # Calculate the total fine fee for all damages found
        total_fine_fee = damage_found.get('Broken', 0) * fine_fee_broken \
                         + damage_found.get('Deformation', 0) * fine_fee_deformation \
                         + damage_found.get('Broken Glass', 0) * fine_fee_broken_glass \
                         + damage_found.get('Scratch', 0) * fine_fee_scratch

        return total_fine_fee
