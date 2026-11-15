from __future__ import annotations

from typing import TYPE_CHECKING
from decimal import Decimal

from delivery.delivery import Delivery
from delivery.courier_delivery import CourierDelivery
from delivery.pickup_delivery import PickupDelivery
from delivery.post_delivery import PostDelivery

if TYPE_CHECKING:
    from order.order import Order


class DeliveryProxy(Delivery):
    ALTERNATIVE_TYPES: tuple[type[Delivery], ...] = (
        CourierDelivery,
        PickupDelivery,
        PostDelivery,
    )

    def __init__(self, real_delivery: Delivery):
        self._real_delivery = real_delivery
        self._chosen_delivery = real_delivery
        self._alternative_deliveries = tuple(delivery_type() for delivery_type in self.ALTERNATIVE_TYPES if delivery_type is not type(self._real_delivery))
        self._cost_cache: dict[tuple, Decimal] = {}
        self._delivery_cache: dict[tuple, Delivery | None] = {}

    def __getattr__(self, attribute: str):
        if self._chosen_delivery is None:
            raise ValueError(f"Delivery for order is unavailable")
        return getattr(self._chosen_delivery, attribute)

    @property
    def name(self) -> str:
        return f"Прокси ({self._real_delivery.name})"

    def get_cost(self, order: Order):
        self.choose_delivery(order)
        chosen_delivery = self._chosen_delivery
        if chosen_delivery is None:
            raise ValueError(f"Delivery for order #{order.id} is unavailable")
        key = (order.id, order.region, order.total_weight, chosen_delivery.name)
        if key in self._cost_cache:
            return self._cost_cache[key]
        cost = chosen_delivery.get_cost(order)
        self._cost_cache[key] = cost
        return cost

    def get_estimated_time(self, order: Order) -> str:
        self.choose_delivery(order)
        chosen_delivery = self._chosen_delivery
        if chosen_delivery is None:
            raise ValueError(f"Delivery for order #{order.id} is unavailable")
        return chosen_delivery.get_estimated_time(order)

    def is_available(self, order: Order) -> bool:
        return self.choose_delivery(order)

    def choose_delivery(self, order: Order) -> bool:
        key = (order.id, order.region, order.total_weight)
        if key in self._delivery_cache:
            chosen_delivery = self._delivery_cache[key]
            if chosen_delivery is None:
                return False
            self._chosen_delivery = chosen_delivery
            return True
        if self._real_delivery.is_available(order):
            self._chosen_delivery = self._real_delivery
            self._delivery_cache[key] = self._real_delivery
            return True
        alternatives_deliveries = self.available_alternatives_deliveries(order)
        if not alternatives_deliveries:
            self._chosen_delivery = None
            self._delivery_cache[key] = None
            return False
        chosen_delivery = min(alternatives_deliveries, key=lambda delivery: delivery.get_cost(order), default=None)
        self._chosen_delivery = chosen_delivery
        self._delivery_cache[key] = chosen_delivery
        return True

    def available_alternatives_deliveries(self, order: Order) -> list[Delivery]:
        available_alternatives_deliveries = [delivery for delivery in self._alternative_deliveries if delivery.is_available(order)]
        return available_alternatives_deliveries
