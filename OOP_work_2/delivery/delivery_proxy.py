from __future__ import annotations

from typing import TYPE_CHECKING
from delivery.delivery import Delivery

if TYPE_CHECKING:
    from order.order import Order


class DeliveryProxy(Delivery):
    def __init__(self):
        super().__init__()
        self._real_delivery = 0

    def get_cost(self, order: Order):
        ...

    def get_estimated_time(self):
        ...

    def is_available(self, order: Order):
        ...