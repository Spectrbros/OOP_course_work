from __future__ import annotations

from typing import TYPE_CHECKING

from discount.discount import Discount
from logging.logger import Logger
from logging.logging_source import LoggingSource

if TYPE_CHECKING:
    from order.order import Order


class FreeDeliveryDiscount(Discount):
    @property
    def name(self) -> str:
        return "Free delivery"

    def apply(self, order: Order) -> None:
        previous_cost = order.delivery_cost
        order.apply_free_delivery_discount()
        Logger().log(LoggingSource.DISCOUNT,f"{self.name}: canceled {previous_cost:.2f} rub.")