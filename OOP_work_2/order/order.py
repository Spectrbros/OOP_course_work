from decimal import Decimal
from order.order_status import OrderStatus
from product.product import Product
from discount.discount import Discount
from delivery.delivery import Delivery


class Order:
    _next_id = 1

    def __init__(self):
        self._id = Order._next_id
        Order._next_id += 1
        self._customer = 0
        self._items = []
        self._status = OrderStatus.PENDING
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

    def set_status(self, new_status: OrderStatus):
        if not isinstance(new_status, OrderStatus):
            raise TypeError("The status must be set to OrderStatus")
        if new_status == self._status:
            return
        if not self._status.can_transition_to(new_status):
            raise ValueError(f"Invalid status transition: {self._status.value} -> {new_status.value}")
        self._status = new_status

    # м.б. просто список возвращать, а не кортеж???
    def get_items(self) -> tuple:
        return tuple(self._items)

    def apply_discount(self, discount: Discount):
        ...

    def set_delivery(self, delivery: Delivery):
        ...