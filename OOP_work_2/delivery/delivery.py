from __future__ import annotations

from typing import TYPE_CHECKING
from decimal import Decimal
from abc import ABC, abstractmethod

from logging.logger import Logger
from logging.logging_source import LoggingSource

if TYPE_CHECKING:
    from order.order import Order


class Delivery(ABC):
    def __lshift__(self, order: Order):
        order.set_delivery(self)
        Logger().log(LoggingSource.DELIVERY,f"Delivery «{self.name}» assigned to order #{order.id}")
        return order

    @property
    @abstractmethod
    def name(self):
        ...

    @abstractmethod
    def get_cost(self, order: Order) -> Decimal:
        ...

    @abstractmethod
    def get_estimated_time(self, order: Order) -> str:
        ...

    @abstractmethod
    def is_available(self, order: Order) -> bool:
        ...
