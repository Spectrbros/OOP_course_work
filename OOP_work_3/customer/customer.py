from decimal import Decimal


class Customer:
    _next_id = 1

    def __init__(self, name: str, age: int, phone_number: int) -> None:
        if name == "":
            raise ValueError("Name can't be empty")
        if age < 0 or age > 150:
            raise ValueError("Age can't be negative or greater than 150")
        if phone_number < 0:
            raise ValueError("Number can't be negative")
        self._id = Customer._next_id
        Customer._next_id += 1
        self._name = name
        self._age = age
        self._phone_number = phone_number
        self._cashback_amount = Decimal("0")

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    def add_cashback(self, amount: Decimal) -> None:
        self._cashback_amount += amount