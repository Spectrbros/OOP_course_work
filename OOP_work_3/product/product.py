from __future__ import annotations

from typing import TYPE_CHECKING
from decimal import Decimal
import copy

from .product_type import ProductType
from .product_category import ProductCategory
from .shared_data import SharedData, Weight

if TYPE_CHECKING:
    from warehouse.warehouse import Warehouse

class Quantity:
    def __init__(self, value: int) -> None:
        if value <= 0:
            raise ValueError("Quantity can't be negative or equal to zero")
        self._value = value

    @property
    def value(self) -> int:
        return self._value

    def change(self, delta: int) -> None:
        new_value = self._value + delta
        if new_value < 0:
            raise ValueError(f"Quantity can't be negative: {self._value} + ({delta}) = {new_value}")
        self._value = new_value


class Price:
    def __init__(self, value: str) -> None:
        if Decimal(value) < 0:
            raise ValueError("Price can't be negative")
        self._value = Decimal(value)

    @property
    def value(self) -> Decimal:
        return self._value

class Product:
    _next_id = 0

    def __init__(self, name: str,  category: ProductCategory, product_type: ProductType, weight: float, quantity: int, price: str) -> None:
        Product._next_id += 1
        self._id = Product._next_id
        self._name = name
        self._category = category
        self._type, self._weight = SharedData.get_data(product_type, Weight(weight))
        self._quantity = Quantity(quantity)
        self._price = Price(price)
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

    def clone(self) -> "Product":
        return Product(self._name, self._category, self._weight, self._quantity, Price(str(self._price.value)))

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def category(self) -> str:
        return self._category.value

    @property
    def type(self) -> str:
        return self._type.value

    @property
    def weight(self) -> float:
        return self._weight

    @property
    def quantity(self) -> int:
        return self._quantity.value

    @property
    def price(self) -> Decimal:
        return self._price.value

    def change_quantity(self, delta: int) -> None:
        self._quantity.change(delta)

    def set_price(self, new_price: Price):
        self._price = new_price

    def transfer_to(self, other: Warehouse):
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
            f"ID: {self.id}\n"
            f"Product name: {self.name}\n"
            f"Category: {self.category}\n"
            f"Type: {self.type}\n"
            f"Weight (kg): {self.weight}\n"
            f"Quantity (units): {self.quantity}\n"
            f"Price (RUB): {self.price}\n"
        )

    def short_info(self) -> str:
        return (
            f"ID: {self._id} | {self.type} | {self.name} | "
            f"price: {self.price} RUB | quantity: {self.quantity} pcs"
        )