from __future__ import annotations

from typing import TYPE_CHECKING
from discount.discount import Discount

if TYPE_CHECKING:
    from order.order import Order


class FreeDeliveryDiscount(Discount):
    def apply(self, order: Order) -> None:
        order.