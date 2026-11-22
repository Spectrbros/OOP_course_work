from abc import ABC
import copy

from product.product import Product
class Electronics(Product, ABC):
    def __init__(self, name, price, quantity, weight):
        super().__init__(name, "electronics", price, quantity, weight)


class Clothing(Product, ABC):
    def __init__(self, name, price, quantity, weight):
        super().__init__(name, "clothing", price, quantity, weight)


class Food(Product, ABC):
    def __init__(self, name, price, quantity, weight):
        super().__init__(name, "food", price, quantity, weight)


class Smartphone(Electronics):
    def __init__(self, name, price,quantity,weight):
        super().__init__(name, price, quantity, weight)

    def clone(self) -> "Product":
        return copy.deepcopy(self)


class Laptop(Electronics):
    def __init__(self, name, price,quantity,weight):
        super().__init__(name, price, quantity, weight)

    def clone(self) -> "Product":
        return copy.deepcopy(self)


class TShirt(Clothing):
    def __init__(self, name, price,quantity,weight):
        super().__init__(name, price, quantity, weight)

    def clone(self) -> "Product":
        return copy.deepcopy(self)


class Jacket(Clothing):
    def __init__(self, name, price,quantity,weight):
        super().__init__(name, price, quantity, weight)

    def clone(self) -> "Product":
        return copy.deepcopy(self)


class Milk(Food):
    def __init__(self, name, price,quantity,weight):
        super().__init__(name, price, quantity, weight)

    def clone(self) -> "Product":
        return copy.deepcopy(self)


class Bread(Food):
    def __init__(self, name, price,quantity,weight):
        super().__init__(name, price, quantity, weight)

    def clone(self) -> "Product":
        return copy.deepcopy(self)