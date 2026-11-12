from __future__ import annotations

from typing import TYPE_CHECKING
from discount.discount import Discount
from product.product import Product, Quantity, CurrentPrice
import random

if TYPE_CHECKING:
    from order.order import Order


class GiftDiscount(Discount):
    _gifts = ("mug", "book", "headphones")

    @property
    def name(self):
        return "Free gift"

    def apply(self, order: Order) -> None:
        gift = Product(random.choice(self._gifts), Quantity(1), CurrentPrice("0"))
        order.apply_gift_discount(gift)