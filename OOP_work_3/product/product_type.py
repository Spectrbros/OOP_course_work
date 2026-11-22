from __future__ import annotations

from product_category import ProductCategory

class Weight:
    def __init__(self, value: float) -> None:
        if value < 0:
            raise ValueError("Weight can't be negative")
        self._value = value

    @property
    def value(self) -> float:
        return self._value

class ProductType:
    _pool: dict[tuple[ProductCategory, Weight], ProductType] = {}

    def __init__(self, category: ProductCategory, weight: Weight) -> None:
        self._category = category
        self._weight = weight

    @classmethod
    def get_type(cls, category: ProductCategory, weight: Weight) -> tuple:
        key = (category, weight)
        if key not in cls._pool:
            cls._pool[key] = cls(category, weight)
        value= cls._pool[key]
        data = (value.category, value.weight)
        return data

    @property
    def category(self) -> str:
        return self._category.value

    @property
    def weight(self) -> float:
        return self._weight.value