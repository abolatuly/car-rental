import uuid
from typing import Protocol

from payments import models, repos


class BillServicesInterface(Protocol):

    def pay_bill(self, order_id: uuid.UUID) -> None:
        ...

    def get_bill(self, order_id: uuid.UUID) -> models.Bill:
        ...


class BillServicesV1:
    bill_repos: repos.BillReposInterface = repos.BillReposV1()

    def pay_bill(self, order_id: uuid.UUID) -> None:
        self.bill_repos.pay_bill(order_id=order_id)

    def get_bill(self, order_id: uuid.UUID) -> models.Bill:
        return self.bill_repos.get_bill(order_id=order_id)
