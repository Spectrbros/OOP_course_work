from __future__ import annotations

from typing import TYPE_CHECKING
from decimal import Decimal
from abc import ABC, abstractmethod
from order.order import Order

if TYPE_CHECKING:
    from order.order import Order


class Delivery(ABC):
    def __lshift__(self, order: Order):
        order.set_delivery(self)
        return order

    @abstractmethod
    def get_cost(self, order: Order) -> Decimal:
        ...

    @abstractmethod
    def get_estimated_time(self) -> str:
        ...

    @abstractmethod
    def is_available(self, order: Order) -> bool:
        ...
