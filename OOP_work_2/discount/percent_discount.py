from __future__ import annotations

from typing import TYPE_CHECKING
from decimal import Decimal
from discount.discount import Discount

if TYPE_CHECKING:
    from order.order import Order


class PercentDiscount(Discount):
    def __init__(self, percent: float):
        if percent <= 0:
            raise ValueError("Percent discount can't be negative or equal to zero")
        self._percent = Decimal(str(percent))

    def apply(self, order: Order) -> None:
        order.apply_percent_discount(self._percent)