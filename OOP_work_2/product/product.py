from decimal import Decimal
from product_type import ProductType


class Quantity:
    def __init__(self, value: int) -> None:
        if value <= 0:
            raise ValueError("Quantity can't be negative or equal to zero.")
        self._value = value

    @property
    def value(self) -> int:
        return self._value

    def change(self, delta: int) -> None:
        new_value = self._value + delta
        if new_value < 0:
            raise ValueError(f"Quantity can't be negative: {self._value} + ({delta}) = {new_value}")
        self._value = new_value


class CurrentPrice:
    def __init__(self, value: str) -> None:
        if Decimal(value) <= 0:
            raise ValueError("Price can't be negative or equal to zero.")
        self._value = Decimal(value)

    @property
    def value(self) -> Decimal:
        return self._value


class Product:
    _next_id = 1

    def __init__(self, category: str, quantity: Quantity, current_price: CurrentPrice) -> None:
        self._id = Product._next_id
        Product._next_id += 1
        self._quantity = quantity # количество товара в ЗАКАЗЕ (НЕ НА СКЛАДЕ)
        self._current_price = current_price
        self._type = ProductType.get_type(category)

    @property
    def id(self) -> int:
        return self._id

    @property
    def weight(self) -> float:
        return self._type.base_weight * self._quantity.value

    @property
    def total_price(self) -> Decimal:
        return self._current_price.value * self._quantity.value

    @property
    def quantity(self) -> int:
        return self._quantity.value

    def change_quantity(self, delta: int) -> None:
        self._quantity.change(delta)