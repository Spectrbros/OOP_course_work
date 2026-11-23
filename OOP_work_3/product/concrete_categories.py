from abc import ABC

from .product import Product
from .product_category import ProductCategory
from .product_type import ProductType

class Electronics(Product, ABC):
    def __init__(self, name, product_type: ProductType, weight, quantity, price):
        super().__init__(name, ProductCategory.ELECTRONICS, product_type, weight, quantity, price)


class Clothing(Product, ABC):
    def __init__(self, name, product_type: ProductType, weight, quantity, price):
        super().__init__(name, ProductCategory.CLOTHING, product_type, weight, quantity, price)


class Food(Product, ABC):
    def __init__(self, name, product_type: ProductType, weight, quantity, price):
        super().__init__(name, ProductCategory.FOOD, product_type, weight, quantity, price)