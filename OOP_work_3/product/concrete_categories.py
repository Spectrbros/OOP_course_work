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


class Home(Product, ABC):
    def __init__(self, name, product_type: ProductType, weight, quantity, price):
        super().__init__(name, ProductCategory.HOME, product_type, weight, quantity, price)


class Books(Product, ABC):
    def __init__(self, name, product_type: ProductType, weight, quantity, price):
        super().__init__(name, ProductCategory.BOOKS, product_type, weight, quantity, price)


class Sports(Product, ABC):
    def __init__(self, name, product_type: ProductType, weight, quantity, price):
        super().__init__(name, ProductCategory.SPORTS, product_type, weight, quantity, price)


class Beauty(Product, ABC):
    def __init__(self, name, product_type: ProductType, weight, quantity, price):
        super().__init__(name, ProductCategory.BEAUTY, product_type, weight, quantity, price)


class Tools(Product, ABC):
    def __init__(self, name, product_type: ProductType, weight, quantity, price):
        super().__init__(name, ProductCategory.TOOLS, product_type, weight, quantity, price)


class Toys(Product, ABC):
    def __init__(self, name, product_type: ProductType, weight, quantity, price):
        super().__init__(name, ProductCategory.TOYS, product_type, weight, quantity, price)