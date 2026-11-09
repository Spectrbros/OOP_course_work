from __future__ import annotations

from typing import TYPE_CHECKING
from delivery.delivery import Delivery

if TYPE_CHECKING:
    from order.order import Order


class CourierDelivery(Delivery):
    _BASE_COST = 500.0
    _COST_PER_KG = 20.0
    _FREE_KG = 10.0
    _MAX_WEIGHT = 20.0
    _TIME = "1-2 days"

    def get_cost(self, order: Order):
        order_weight = order.get_total_weight()
        extra = max(0.0, order_weight - self._FREE_KG) * self._COST_PER_KG
        return self._BASE_COST + extra

    def get_estimated_time(self) -> str:
        return self._TIME

    def is_available(self, order: Order) -> bool:
        return order.get_total_weight() <= self._MAX_WEIGHT