from abc import ABC, abstractmethod

from .product import Product


class ProductFactory(ABC):
    @abstractmethod
    def create_product(self, name: str, weight: float, quantity: int, price: str) -> Product:
        ...
