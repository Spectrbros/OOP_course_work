from __future__ import annotations

from .product_type import ProductType


class Weight:
    def __init__(self, value: float) -> None:
        if value < 0:
            raise ValueError("Weight can't be negative")
        self._value = value

    @property
    def value(self) -> float:
        return self._value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Weight):
            return NotImplemented
        return self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)


class SharedData:
    _pool: dict[tuple[ProductType, Weight], SharedData] = {}

    def __init__(self, product_type: ProductType, weight: Weight) -> None:
        self._type = product_type
        self._weight = weight

    @classmethod
    def get_data(cls, product_type: ProductType, weight: Weight) -> tuple:
        key = (product_type, weight)
        if key not in cls._pool:
            cls._pool[key] = cls(product_type, weight)
        value= cls._pool[key]
        data = (value.type, value.weight)
        return data

    @property
    def type(self) -> ProductType:
        return self._type

    @property
    def weight(self) -> float:
        return self._weight.value