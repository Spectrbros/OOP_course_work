from abc import ABC, abstractmethod

class ProductFactory(ABC):
    @abstractmethod
    def create_product(self, name: str, price: int, quantity: int, weight: float) -> Product:
        ...

