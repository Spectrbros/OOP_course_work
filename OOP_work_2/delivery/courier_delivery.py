from __future__ import annotations

from typing import TYPE_CHECKING
from decimal import Decimal
from delivery.delivery import Delivery

if TYPE_CHECKING:
    from order.order import Order


class CourierDelivery(Delivery):
    _BASE_COST = Decimal("500")
    _COST_PER_KG = Decimal("20")
    _FREE_KG = 10.0
    _MAX_WEIGHT = 20.0
    _TIME = "1-2 days"

    @property
    def name(self):
        return "Courier"

    def get_cost(self, order: Order) -> Decimal:
        order_weight = order.total_weight
        extra = Decimal(str(max(0.0, order_weight - self._FREE_KG))) * self._COST_PER_KG
        return self._BASE_COST + extra

    def get_estimated_time(self) -> str:
        return self._TIME

    def is_available(self, order: Order) -> bool:
        return order.total_weight <= self._MAX_WEIGHT