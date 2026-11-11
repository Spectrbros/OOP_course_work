from decimal import Decimal


class Customer:
    _next_id = 1

    def __init__(self, name: str, age: int) -> None:
        self._id = Customer._next_id
        Customer._next_id += 1
        self._name = name
        self._age = age
        self._cashback_amount = Decimal("0")

    def add_cashback(self, amount: Decimal) -> None:
        self._cashback_amount += amount