from __future__ import annotations

from typing import TYPE_CHECKING
from decimal import Decimal
from discount.discount import Discount

if TYPE_CHECKING:
    from order.order import Order


class CashbackDiscount(Discount):
    def __init__(self, percent: float):
        if percent <= 0:
            raise ValueError("Cashback discount percent can't be negative or equal to zero")
        self._cashback_percent = Decimal(str(percent))

    def apply(self, order: Order) -> None:
        order.apply_cashback_discount(self._cashback_percent)