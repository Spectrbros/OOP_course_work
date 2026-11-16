from __future__ import annotations

from typing import TYPE_CHECKING
from decimal import Decimal

from discount.discount import Discount
from logging.logger import Logger
from logging.logging_source import LoggingSource

if TYPE_CHECKING:
    from order.order import Order


class CashbackDiscount(Discount):
    def __init__(self, percent: str = "5") -> None:
        percent = Decimal(percent)
        if percent <= 0 or percent > 100:
            raise ValueError("Cashback discount can only be in the range of 0% to 100%.")
        self._cashback_percent = percent

    @property
    def name(self) -> str:
        return f"{self._cashback_percent}% cashback"

    def apply(self, order: Order) -> None:
        amount = order.total_price * (self._cashback_percent / 100)
        order.apply_cashback_discount(amount)
        Logger().log(LoggingSource.DISCOUNT, f"{self.name}: accrued {amount:.2f} rub.")