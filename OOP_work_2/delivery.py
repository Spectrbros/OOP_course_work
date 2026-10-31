from abc import ABC, abstractmethod
from order import Order

class Delivery(ABC):
    def __init__(self):
        ...

    @abstractmethod
    def get_cost(self, order: Order):
        ...
    @abstractmethod
    def get_estimated_time(self):
        ...
    @abstractmethod
    def is_available(self, order: Order):
        ...
