from __future__ import annotations

from typing import TYPE_CHECKING
from decimal import Decimal
from delivery.delivery import Delivery

if TYPE_CHECKING:
    from order.order import Order


class PostDelivery(Delivery):
    _BASE_COST = Decimal("200")
    _COST_PER_KG = Decimal("30")
    _FREE_KG = 5.0
    _MAX_WEIGHT = 10.0
    _TIME = "5-10 days"

    def get_cost(self, order: Order) -> Decimal:
        order_weight = order.get_total_weight()
        extra = Decimal(str(max(0.0, order_weight - self._FREE_KG))) * self._COST_PER_KG
        return self._BASE_COST + extra

    def get_estimated_time(self) -> str:
        return self._TIME

    def is_available(self, order: Order) -> bool:
        return order.get_total_weight() <= self._MAX_WEIGHT