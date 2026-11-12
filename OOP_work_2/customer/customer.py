from decimal import Decimal


class Customer:
    _next_id = 1

    def __init__(self, name: str, age: int, phone_number: int, email: str) -> None:
        self._id = Customer._next_id
        Customer._next_id += 1
        self._name = name
        self._age = age
        self._phone_number = phone_number
        self._email = email
        self._cashback_amount = Decimal("0")

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def add_cashback(self, amount: Decimal) -> None:
        self._cashback_amount += amount