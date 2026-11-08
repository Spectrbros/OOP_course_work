from abc import ABC, abstractmethod
from order import Order

class Discount(ABC):
    @abstractmethod
    def apply(self, order: Order):
        ...
