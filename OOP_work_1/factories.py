from products import Product, Smartphone, Laptop, TShirt, Jacket, Milk, Bread
from abc import ABC, abstractmethod

class ProductFactory(ABC):
    @abstractmethod
    def create_product(self, name: str, price: int, quantity: int, weight: float) -> Product:
        ...

class SmartphoneFactory(ProductFactory):
    def create_product(self, name: str, price: int, quantity: int, weight: float) -> Product:
        return Smartphone(name, price, quantity, weight)

class LaptopFactory(ProductFactory):
    def create_product(self, name: str, price: int, quantity: int, weight: float) -> Product:
        return Laptop(name, price, quantity, weight)

class TShirtFactory(ProductFactory):
    def create_product(self, name: str, price: int, quantity: int, weight: float) -> Product:
        return TShirt(name, price, quantity, weight)

class JacketFactory(ProductFactory):
    def create_product(self, name: str, price: int, quantity: int, weight: float) -> Product:
        return Jacket(name, price, quantity, weight)

class MilkFactory(ProductFactory):
    def create_product(self, name: str, price: int, quantity: int, weight: float) -> Product:
        return Milk(name, price, quantity, weight)

class BreadFactory(ProductFactory):
    def create_product(self, name: str, price: int, quantity: int, weight: float) -> Product:
        return Bread(name, price, quantity, weight)