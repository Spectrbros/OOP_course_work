from decimal import Decimal

from product.catalog import catalog_initialization
from product.product_category import ProductCategory
from product.product_type import ProductType


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


class CurrentPrice:
    def __init__(self, value: str) -> None:
        if Decimal(value) < 0:
            raise ValueError("Price can't be negative")
        self._value = Decimal(value)

    @property
    def value(self) -> Decimal:
        return self._value


class Product:
    _next_id = 1

    def __init__(self, category: ProductCategory | str, quantity: Quantity, current_price: CurrentPrice) -> None:
        self._id = Product._next_id
        Product._next_id += 1
        self._quantity = quantity
        self._current_price = current_price
        if isinstance(category, ProductCategory):
            category = category.title
        self._type = ProductType.get_type(category)

    def __str__(self) -> str:
        return f"{self._type.category} x{self._quantity.value} | {self.total_price:.2f} RUB"

    def clone(self) -> "Product":
        return Product(self._type.category, Quantity(self._quantity.value), CurrentPrice(str(self._current_price.value)))

    @classmethod
    def from_category(cls, category: ProductCategory, quantity: int, price: str | None = None) -> "Product":
        catalog_initialization()
        price_str = category.base_price if price is None else price
        return cls(category, Quantity(quantity), CurrentPrice(price_str))

    @property
    def id(self) -> int:
        return self._id

    @property
    def weight(self) -> float:
        return self._type.base_weight.value * self._quantity.value

    @property
    def total_price(self) -> Decimal:
        return self._current_price.value * self._quantity.value

    @property
    def quantity(self) -> int:
        return self._quantity.value

    @property
    def type(self):
        return self._type

    def change_quantity(self, delta: int) -> None:
        self._quantity.change(delta)