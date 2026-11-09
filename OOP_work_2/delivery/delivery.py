from __future__ import annotations

from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from order.order import Order


class Delivery(ABC):
    @abstractmethod
    def get_cost(self, order: Order):
        ...

    @abstractmethod
    def get_estimated_time(self):
        ...

    @abstractmethod
    def is_available(self, order: Order):
        ...
