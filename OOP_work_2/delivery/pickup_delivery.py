from __future__ import annotations

from typing import TYPE_CHECKING
from decimal import Decimal
from delivery.delivery import Delivery

if TYPE_CHECKING:
    from order.order import Order


class PickupDelivery(Delivery):
    _BASE_COST = Decimal("0")
    _TIME = "1-3 days"

    @property
    def name(self):
        return "Pickup"

    def get_cost(self, order: Order) -> Decimal:
        return self._BASE_COST

    def get_estimated_time(self) -> str:
        return self._TIME

    def is_available(self, order: Order) -> bool:
        return True