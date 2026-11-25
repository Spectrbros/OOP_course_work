from __future__ import annotations

from typing import TYPE_CHECKING
import random

from discount.discount import Discount
from product.product import Product
from product.concrete_products import Mug, Book, Headphones
from product.concrete_factories import MugFactory, BookFactory, HeadphonesFactory
from logging_service.logger import Logger
from logging_service.logging_source import LoggingSource

if TYPE_CHECKING:
    from order.order import Order


class GiftDiscount(Discount):
    _free_gifts_list = (
        (MugFactory, "Gift mug", 0.4),
        (BookFactory, "Gift book", 0.5),
        (HeadphonesFactory, "Gift headphones", 0.3),
    )

    @property
    def name(self) -> str:
        return "Free gift"

    def apply(self, order: Order) -> None:
        factory_class, gift_name, gift_weight = random.choice(self._free_gifts_list)
        random_free_gift = factory_class().create_product(gift_name, gift_weight, 1, "0")
        order.apply_gift_discount(random_free_gift)
        Logger().log(LoggingSource.DISCOUNT,f"A gift has been added to order #{order.id}: {random_free_gift.type} x{random_free_gift.quantity}")