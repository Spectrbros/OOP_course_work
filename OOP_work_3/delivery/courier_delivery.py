from __future__ import annotations

from typing import TYPE_CHECKING
from decimal import Decimal

from delivery.delivery import Delivery
from delivery.delivery_region import DeliveryRegion

if TYPE_CHECKING:
    from order.order import Order


class CourierDelivery(Delivery):
    _BASE_COST = Decimal("500")
    _COST_PER_KG = Decimal("20")
    _FREE_KG = Decimal("10")
    _MAX_WEIGHT = 20.0
    _TIME = "1-2 days"
    _SUPPORTED_REGIONS = {DeliveryRegion.MOSCOW,
                          DeliveryRegion.SAINT_PETERSBURG,
                          DeliveryRegion.KAZAN,
                          DeliveryRegion.NOVOSIBIRSK,
                          DeliveryRegion.YEKATERINBURG,
                          DeliveryRegion.NIZHNY_NOVGOROD}

    @property
    def name(self) -> str:
        return "Courier"

    def get_cost(self, order: Order) -> Decimal:
        order_weight = Decimal(str(order.total_weight))
        extra = max(Decimal("0"), order_weight - self._FREE_KG) * self._COST_PER_KG
        return self._BASE_COST + extra

    def get_estimated_time(self, order: Order | None) -> str:
        return self._TIME

    def is_available(self, order: Order) -> bool:
        return order.total_weight <= self._MAX_WEIGHT and order.region in self._SUPPORTED_REGIONS