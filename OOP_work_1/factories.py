from abc import ABC, abstractmethod

class ProductFactory(ABC):
    def create_product(self, id: int, name: str, price: int, quantity: int, weight: float):
        ...

class SmartphoneFactory(ProductFactory):
    def create_product(self, id: int, name: str, price: int, quantity: int, weight: float):
        ...

class LaptopFactory(ProductFactory):
    def create_product(self, id: int, name: str, price: int, quantity: int, weight: float):
        ...

class TShirtFactory(ProductFactory):
    def create_product(self, id: int, name: str, price: int, quantity: int, weight: float):
        ...

class JacketFactory(ProductFactory):
    def create_product(self, id: int, name: str, price: int, quantity: int, weight: float):
        ...

class MilkFactory(ProductFactory):
    def create_product(self, id: int, name: str, price: int, quantity: int, weight: float):
        ...

class BreadFactory(ProductFactory):
    def create_product(self, id: int, name: str, price: int, quantity: int, weight: float):
        ...