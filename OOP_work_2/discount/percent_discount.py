from __future__ import annotations

from typing import TYPE_CHECKING
from discount.discount import Discount

if TYPE_CHECKING:
    from order.order import Order


class PercentDiscount(Discount):
    def __init__(self):
        self._percent = 10.0

    def apply(self, order: Order) -> None:
        order.apply_percent_discount(self._percent)