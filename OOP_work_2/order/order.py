from decimal import Decimal
from product.product import Product

class Order:
    _next_id = 1

    def __init__(self):
        self._id = Order._next_id
        Order._next_id += 1
        self._customer = 0
        self._items = []
        self._status = 0
        self._delivery = 0
        self._discounts = 0
        self._total_price = 0

    def add_item(self, item: Product):
        self._items.append(item)

    def remove_item(self, id: int):
        if id < 1:
            raise ValueError("Product ID doesn't exist")
        for index, item in enumerate(self._items):
            if item.id == id:
                del self._items[index]
                return
        raise ValueError("There is no product with this ID in the order.")

    def get_total_weight(self) -> float:
        total_weight = 0
        for item in self._items:
            total_weight += item.weight
        return total_weight

    def get_total_price(self) -> Decimal:
        total_price = Decimal("0")
        for item in self._items:
            total_price += item.total_price
        return total_price

    def set_status(self, status: str):
        if status in {"pending", "paid", "shipped", "delivered", "cancelled"}:
            self._status = status
        else:
            raise ValueError("Invalid status name")