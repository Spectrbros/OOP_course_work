from __future__ import annotations

from typing import TYPE_CHECKING
from decimal import Decimal

from delivery.delivery import Delivery
from delivery.delivery_region import DeliveryRegion

if TYPE_CHECKING:
    from order.order import Order


class PickupDelivery(Delivery):
    _BASE_COST = Decimal("0")
    _TIME = "1-3 days"
    _SUPPORTED_REGIONS = {DeliveryRegion.MOSCOW,
                          DeliveryRegion.SAINT_PETERSBURG,
                          DeliveryRegion.KAZAN,
                          DeliveryRegion.NOVOSIBIRSK,
                          DeliveryRegion.YEKATERINBURG,
                          DeliveryRegion.NIZHNY_NOVGOROD}

    @property
    def name(self):
        return "Pickup"

    def get_cost(self, order: Order) -> Decimal:
        return self._BASE_COST

    def get_estimated_time(self, order: Order | None) -> str:
        return self._TIME

    def is_available(self, order: Order) -> bool:
        return order.region in self._SUPPORTED_REGIONS