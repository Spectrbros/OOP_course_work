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

    def change(self, delta: int):
        new_value = self._value + delta
        if new_value < 0:
            raise ValueError(f"Quantity can't be negative: {self._value} + ({delta}) = {new_value}")
        self._value = new_value


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
    _next_id = 0

    def __init__(self, name: str, category: str, price: int, quantity: int, weight: float):
        Product._next_id += 1
        self._id = Product._next_id
        self._name = name
        self._category = category
        self._price = Price(price)
        self._quantity = Quantity(quantity)
        self._weight = Weight(weight)
        self._warehouse = None

    def __deepcopy__(self, memo):
        cls = type(self)
        result = cls.__new__(cls)
        memo[id(self)] = result

        for key, value in self.__dict__.items():
            if key == "_warehouse":
                setattr(result, key, None)
            else:
                setattr(result, key, copy.deepcopy(value, memo))

        return result

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

    def change_quantity(self, delta: int):
        self._quantity.change(delta)

    def set_price(self, new_price: Price):
        self._price = new_price

    def transfer_to(self, other: "Warehouse"):
        if self._warehouse is other:
            return
        if other is None:
            raise ValueError("Warehouse for transfer isn't specified")

        if self._warehouse is None:
            other.add_product(self)
        else:
            old_warehouse = self._warehouse
            other.add_product(self)
            old_warehouse.remove_by_id(self._id)

    def info(self) -> str:
        return (
            f"ID: {self._id}\n"
            f"Наименование товара: {self._name}\n"
            f"Категория: {self._category}\n"
            f"Цена (руб): {self._price.value}\n"
            f"Количество (шт): {self._quantity.value}\n"
            f"Вес (кг): {self._weight.value}\n"
        )


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