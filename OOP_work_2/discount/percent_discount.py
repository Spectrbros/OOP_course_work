from __future__ import annotations

from typing import TYPE_CHECKING
from decimal import Decimal

from discount.discount import Discount
from logging.logger import Logger
from logging.logging_source import LoggingSource

if TYPE_CHECKING:
    from order.order import Order


class PercentDiscount(Discount):
    def __init__(self, percent: str = "10") -> None:
        percent = Decimal(percent)
        if percent <= 0 or percent > 100:
            raise ValueError("The discount can only be in the range of 0% to 100%.")
        self._percent = percent

    @property
    def name(self) -> str:
        return f"{self._percent}% percent discount"

    def apply(self, order: Order) -> None:
        amount = order.total_price * (self._percent / 100)
        order.apply_percent_discount(amount)
        Logger().log(LoggingSource.DISCOUNT,f"{self.name}: discount of {amount:.2f} RUB")