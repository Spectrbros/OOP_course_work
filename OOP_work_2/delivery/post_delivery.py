from __future__ import annotations

from typing import TYPE_CHECKING
from delivery.delivery import Delivery

if TYPE_CHECKING:
    from order.order import Order


class PostDelivery(Delivery):
    _BASE_COST = 200.0
    _COST_PER_KG = 30.0
    _FREE_KG = 5.0
    _MAX_WEIGHT = 10.0
    _TIME = "5-10 days"

    def get_cost(self, order: Order):
        order_weight = order.get_total_weight()
        extra = max(0.0, order_weight - self._FREE_KG) * self._COST_PER_KG
        return self._BASE_COST + extra

    def get_estimated_time(self) -> str:
        return self._TIME

    def is_available(self, order: Order) -> bool:
        return order.get_total_weight() <= self._MAX_WEIGHT