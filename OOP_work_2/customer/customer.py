from decimal import Decimal


class Customer:
    _next_id = 1

    def __init__(self, name: str, age: int) -> None:
        self._id = Customer._next_id
        Customer._next_id += 1
        self._name = name
        self._age = age
        self._cashback_amount = Decimal("0")
        self._active_orders_count = 0

    def add_cashback(self, amount: Decimal) -> None:
        self._cashback_amount += amount

    @property
    def active_orders_count(self):
        return self._active_orders_count

    @active_orders_count.setter
    def active_orders_count(self, delta: int):
        new_value = self._active_orders_count + delta
        if new_value< 0:
            raise ValueError(f"Active orders count can't be negative: {self._active_orders_count} + ({delta}) = {new_value}")
        self._active_orders_count = new_value