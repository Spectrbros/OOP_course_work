from __future__ import annotations

from typing import TYPE_CHECKING
from discount.discount import Discount

if TYPE_CHECKING:
    from order.order import Order


class FreeDeliveryDiscount(Discount):
    @property
    def name(self):
        return "Free delivery"

    def apply(self, order: Order) -> None:
        order.apply_free_delivery_discount()