from abc import ABC, abstractmethod
import copy

class Price:
    def __init__(self, val: int):
        if val < 0:
            raise ValueError("Price can't be negative")
        self._value = val

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, val: int):
        if val < 0:
            raise ValueError("Price can't be negative")
        self._value = val


class Quantity:
    def __init__(self, val: int):
        if val < 0:
            raise ValueError("Quantity can't be negative")
        self._value = val

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, val: int):
        if val < 0:
            raise ValueError("Quantity can't be negative")
        self._value = val


class Weight:
    def __init__(self, val: float):
        if val < 0:
            raise ValueError("Weight can't be negative")
        self._value = val

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, val: float):
        if val < 0:
            raise ValueError("Weight can't be negative")
        self._value = val


class Product(ABC):
    _count = 0

    def __init__(self, name: str, category: str, price: int, quantity: int, weight: float):
        self._id = Product._count + 1
        Product._count += 1
        self._name = name
        self._category = category
        self._price = Price(price)
        self._quantity = Quantity(quantity)
        self._weight = Weight(weight)

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def category(self) -> str:
        return self._category

    @property
    def price(self) -> Price:
        return self._price

    @property
    def quantity(self) -> Quantity:
        return self._quantity

    @property
    def weight(self) -> Weight:
        return self._weight

    @abstractmethod
    def clone(self) -> "Product":
        ...


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