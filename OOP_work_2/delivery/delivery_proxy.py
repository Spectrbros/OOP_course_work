from __future__ import annotations

from typing import TYPE_CHECKING
from decimal import Decimal

from delivery.delivery import Delivery
from delivery.courier_delivery import CourierDelivery
from delivery.pickup_delivery import PickupDelivery
from delivery.post_delivery import PostDelivery
from logging.logger import Logger
from logging.logging_source import LoggingSource

if TYPE_CHECKING:
    from order.order import Order


class DeliveryProxy(Delivery):
    ALTERNATIVE_TYPES: tuple[type[Delivery], ...] = (
        CourierDelivery,
        PickupDelivery,
        PostDelivery,
    )

    def __init__(self, real_delivery: Delivery) -> None:
        self._real_delivery = real_delivery
        self._chosen_delivery: Delivery | None = real_delivery
        self._alternative_deliveries = tuple(delivery_type() for delivery_type in self.ALTERNATIVE_TYPES if delivery_type is not type(self._real_delivery))
        self._cost_cache: dict[tuple, Decimal] = {}
        self._delivery_cache: dict[tuple, Delivery | None] = {}
        self._logger = Logger()

    def __getattr__(self, attribute: str):
        if self._chosen_delivery is None:
            raise ValueError(f"Delivery for order is unavailable")
        return getattr(self._chosen_delivery, attribute)

    @property
    def name(self) -> str:
        return f"Прокси ({self._chosen_delivery.name})"

    def get_cost(self, order: Order) -> Decimal:
        self.choose_delivery(order)
        chosen_delivery = self._chosen_delivery
        if chosen_delivery is None:
            self._logger.log(LoggingSource.DELIVERY,"There are no available delivery methods for order #{order.id}")
            raise ValueError(f"Delivery for order #{order.id} is unavailable")
        if chosen_delivery is not self._real_delivery:
            self._logger.log(LoggingSource.DELIVERY,f"Delivery method «{self._real_delivery.name}» is not available, chosen «{chosen_delivery.name}»",
            )
        key = (order.id, order.region, order.total_weight, chosen_delivery.name)
        if key in self._cost_cache:
            self._logger.log(LoggingSource.DELIVERY,f"Cost from cache: {self._cost_cache[key]:.2f} RUB")
            return self._cost_cache[key]
        cost = chosen_delivery.get_cost(order)
        self._cost_cache[key] = cost
        self._logger.log(LoggingSource.DELIVERY,f"Cost calculation for «{chosen_delivery.name}»: {cost:.2f} RUB")
        return cost

    def get_estimated_time(self, order: Order) -> str:
        self.choose_delivery(order)
        chosen_delivery = self._chosen_delivery
        if chosen_delivery is None:
            raise ValueError(f"Delivery for order #{order.id} is unavailable")
        estimated_time = chosen_delivery.get_estimated_time(order)
        self._logger.log(LoggingSource.DELIVERY,f"Estimated time «{chosen_delivery.name}»: {estimated_time}")
        return estimated_time

    def is_available(self, order: Order) -> bool:
        available = self.choose_delivery(order)
        self._logger.log(LoggingSource.DELIVERY,f"Checking the availability of order #{order.id}: {'available' if available else 'unavailable'}")
        return available

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
