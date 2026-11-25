from decimal import Decimal

from product.product import Product


class OrderItem:
    def __init__(self, product_id: int, name: str, category: str, product_type: str, unit_price, quantity: int, weight: float) -> None:
        if product_id < 1:
            raise ValueError("Product ID can't be less than 1")
        if quantity <= 0:
            raise ValueError("Ordered quantity must be positive")
        price = Decimal(str(unit_price))
        if price < 0:
            raise ValueError("Unit price can't be negative")
        if weight < 0:
            raise ValueError("Weight can't be negative")

        self._product_id = product_id
        self._name = name
        self._category = category
        self._type = product_type
        self._unit_price = price
        self._quantity = quantity
        self._weight = weight

    @classmethod
    def from_product(cls, product: Product, quantity: int | None = None, unit_price=None) -> "OrderItem":
        if quantity is None:
            quantity = product.quantity
        if unit_price is None:
            unit_price = product.price
        return cls(product_id=product.id, name=product.name, category=product.category, product_type=product.type, unit_price=unit_price, quantity=quantity, weight=product.weight)

    @property
    def id(self) -> int:
        return self._product_id

    @property
    def product_id(self) -> int:
        return self._product_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def category(self) -> str:
        return self._category

    @property
    def type(self) -> str:
        return self._type

    @property
    def unit_price(self) -> Decimal:
        return self._unit_price

    @property
    def price(self) -> Decimal:
        return self._unit_price

    @property
    def quantity(self) -> int:
        return self._quantity

    @property
    def weight(self) -> float:
        return self._weight

    @property
    def total_price(self) -> Decimal:
        return self._unit_price * self._quantity

    @property
    def total_weight(self) -> float:
        return self._weight * self._quantity

    def clone(self) -> "OrderItem":
        return OrderItem(product_id=self._product_id, name=self._name, category=self._category, product_type=self._type, unit_price=self._unit_price, quantity=self._quantity, weight=self._weight)
