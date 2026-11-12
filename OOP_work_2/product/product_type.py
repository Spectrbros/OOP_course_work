from __future__ import annotations

from decimal import Decimal


class BaseWeight:
    def __init__(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Weight can't be negative or equal to zero")
        self._value = value

    @property
    def value(self) -> float:
        return self._value


class BasePrice:
    def __init__(self, value: str) -> None:
        if Decimal(value) <= 0:
            raise ValueError("Price can't be negative or equal to zero")
        self._value = Decimal(value)

    @property
    def value(self) -> Decimal:
        return self._value


class ProductType:
    _pool: dict[str, ProductType] = {}
    _catalog: dict[str, tuple[BaseWeight, BasePrice]] = {}

    def __init__(self, category: str, base_weight: BaseWeight, base_price: BasePrice) -> None:
        self._category = category
        self._base_weight = base_weight
        self._base_price = base_price

    @classmethod
    def get_type(cls, category: str) -> ProductType:
        if category not in cls._catalog:
            raise ValueError(f"Unknown product category: {category}")
        if category not in cls._pool:
            base_weight, base_price = cls._catalog[category]
            cls._pool[category] = cls(category, base_weight, base_price)
        return cls._pool[category]

    @classmethod
    def register_type(cls, category: str, base_weight: BaseWeight, base_price: BasePrice) -> None:
        if category in cls._pool:
            raise ValueError(f"Category «{category}» exists in the pool and can't be changed")
        cls._catalog[category] = (base_weight, base_price)

    @property
    def category(self):
        return self._category

    @property
    def base_weight(self) -> BaseWeight:
        return self._base_weight

    @property
    def base_price(self) -> BasePrice:
        return self._base_price