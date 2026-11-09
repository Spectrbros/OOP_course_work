from __future__ import annotations

from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from order.order import Order


class Discount(ABC):
    @abstractmethod
    def apply(self, order: Order):
        ...
