from .product import Product
from .concrete_products import Smartphone, Laptop, TShirt, Jacket, Milk, Bread
from .product_factory import ProductFactory

class SmartphoneFactory(ProductFactory):
    def create_product(self, name: str, weight, quantity, price) -> Product:
        return Smartphone(name, weight, quantity, price)

class LaptopFactory(ProductFactory):
    def create_product(self, name: str, weight, quantity, price) -> Product:
        return Laptop(name, weight, quantity, price)

class TShirtFactory(ProductFactory):
    def create_product(self, name: str, weight, quantity, price) -> Product:
        return TShirt(name, weight, quantity, price)

class JacketFactory(ProductFactory):
    def create_product(self, name: str, weight, quantity, price) -> Product:
        return Jacket(name, weight, quantity, price)

class MilkFactory(ProductFactory):
    def create_product(self, name: str, weight, quantity, price) -> Product:
        return Milk(name, weight, quantity, price)

class BreadFactory(ProductFactory):
    def create_product(self, name: str, weight, quantity, price) -> Product:
        return Bread(name, weight, quantity, price)