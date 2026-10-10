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
        if self._value < 0:
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
        if self._value < 0:
            raise ValueError("Quantity can't be negative")
        self._value = val


class Weight:
    def __init__(self, val: int):
        if val < 0:
            raise ValueError("Weight can't be negative")
        self._value = val

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, val: int):
        if self._value < 0:
            raise ValueError("Weight can't be negative")
        self._value = val


class Product(ABC):
    _count = 0

    def __init__(self, name: str, category: str, price: Price, quantity: Quantity, weight: Weight):
        self._id = Product._count + 1
        Product._count += 1
        self._name = name
        self._category = category
        self._price = price
        self._quantity = quantity
        self._weight = weight

    @property
    @abstractmethod
    def id(self) -> int:
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def category(self) -> str:
        ...

    @property
    @abstractmethod
    def price(self) -> Price:
        ...

    @property
    @abstractmethod
    def quantity(self):
        ...

    @property
    @abstractmethod
    def weight(self):
        ...

    @abstractmethod
    def clone(self) -> "Product":
        ...

class Electronics(Product, ABC):
    def __init__(self, name, category, price, quantity, weight):
        super().__init__(self, name, "electronics", price, quantity, weight)

class Clothing(Product, ABC):
    def __init__(self, name, category, price, quantity, weight):
        super().__init__(self, name, "clothing", price, quantity, weight)

class Food(Product, ABC):
    def __init__(self, name, category, price, quantity, weight):
        super().__init__(self, name, "food", price, quantity, weight)