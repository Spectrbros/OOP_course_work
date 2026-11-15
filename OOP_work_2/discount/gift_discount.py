from __future__ import annotations

from typing import TYPE_CHECKING
import random

from discount.discount import Discount
from product.product import Product, Quantity, CurrentPrice
from logging.logger import Logger
from logging.logging_source import LoggingSource

if TYPE_CHECKING:
    from order.order import Order


class GiftDiscount(Discount):
    _free_gifts_list = ("mug", "book", "headphones")

    def __init__(self) -> None:
        self._random_free_gift = Product(random.choice(self._free_gifts_list), Quantity(1), CurrentPrice("0"))

    @property
    def name(self) -> str:
        return f"Free gift «{self._random_free_gift.type.category}»"

    def apply(self, order: Order) -> None:
        order.apply_gift_discount(self._random_free_gift)
        Logger().log(LoggingSource.ORDER,f"A gift has been added to order #{order.id}: {self._random_free_gift.type.category} x{self._random_free_gift.quantity}")