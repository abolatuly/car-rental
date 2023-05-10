from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from payments import services, serializers


class BillViewSet(ViewSet):
    bill_services: services.BillServicesInterface = services.BillServicesV1()

    def pay_bill(self, request, *args, **kwargs):
        self.bill_services.pay_bill(order_id=kwargs['order_id'])

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_bill(self, request, *args, **kwargs):
        bill = self.bill_services.get_bill(order_id=kwargs['order_id'])
        data = serializers.BillSerializer(bill).data
        return Response(data)
