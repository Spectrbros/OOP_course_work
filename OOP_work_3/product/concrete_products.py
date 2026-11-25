from .concrete_categories import Electronics, Clothing, Food, Home, Books, Sports, Beauty, Tools, Toys
from .product_type import ProductType


class Smartphone(Electronics):
    def __init__(self, name, weight, quantity, price) -> None:
        super().__init__(name, ProductType.SMARTPHONE,weight, quantity, price)


class Laptop(Electronics):
    def __init__(self, name, weight, quantity, price) -> None:
        super().__init__(name, ProductType.LAPTOP, weight, quantity, price)


class TShirt(Clothing):
    def __init__(self, name, weight, quantity, price) -> None:
        super().__init__(name, ProductType.TSHIRT, weight, quantity, price)


class Jacket(Clothing):
    def __init__(self, name, weight, quantity, price) -> None:
        super().__init__(name, ProductType.JACKET, weight, quantity, price)


class Milk(Food):
    def __init__(self, name, weight, quantity, price) -> None:
        super().__init__(name, ProductType.MILK, weight, quantity, price)


class Bread(Food):
    def __init__(self, name, weight, quantity, price) -> None:
        super().__init__(name, ProductType.BREAD, weight, quantity, price)


class Book(Books):
    def __init__(self, name, weight, quantity, price) -> None:
        super().__init__(name, ProductType.BOOK, weight, quantity, price)


class Mug(Home):
    def __init__(self, name, weight, quantity, price) -> None:
        super().__init__(name, ProductType.MUG, weight, quantity, price)


class Headphones(Electronics):
    def __init__(self, name, weight, quantity, price) -> None:
        super().__init__(name, ProductType.HEADPHONES, weight, quantity, price)