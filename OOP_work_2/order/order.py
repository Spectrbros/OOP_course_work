from decimal import Decimal
from order.order_status import OrderStatus
from product.product import Product
from discount.discount import Discount
from delivery.delivery import Delivery
from customer.customer import Customer


class Order:
    _next_id = 1

    def __init__(self, customer: Customer, items: list[Product]) -> None:
        self._id = Order._next_id
        Order._next_id += 1
        self._customer = customer
        self._items = items
        self._status = OrderStatus.PENDING
        self._delivery = None
        self._free_delivery = False
        self._discounts = []
        self._total_price = Decimal("0")

    def __add__(self, discount: Discount):
        self.apply_discount(discount)
        return self



    def add_item(self, item: Product) -> None:
        self._items.append(item)
        self.update_total_price()

    def remove_item(self, id: int) -> None:
        if id < 1:
            raise ValueError("Product ID doesn't exist")
        for index, item in enumerate(self._items):
            if item.id == id:
                del self._items[index]
                self.update_total_price()
                return
        raise ValueError("There is no product with this ID in the order.")

    # м.б. просто список возвращать, а не кортеж???
    def get_items(self) -> tuple:
        return tuple(self._items)

    def set_status(self, new_status: OrderStatus) -> None:
        if not isinstance(new_status, OrderStatus):
            raise TypeError("The status must be set to OrderStatus")
        if new_status == self._status:
            return
        if not self._status.can_transition_to(new_status):
            raise ValueError(f"Invalid status transition: {self._status.value} -> {new_status.value}")
        self._status = new_status

    def set_delivery(self, delivery: Delivery) -> None:
        self._delivery = delivery
        self.update_total_price()

    def apply_discount(self, discount: Discount) -> None:
        discount.apply(self)
        self.update_total_price()

    def get_total_weight(self) -> float:
        total_weight = 0
        for item in self._items:
            total_weight += item.weight
        return total_weight

    def get_total_price(self) -> Decimal:
        total_price = Decimal("0")
        for item in self._items:
            total_price += item.total_price
        if not self._free_delivery and self._delivery is not None:
            total_price += self._delivery.get_cost(self)
        return total_price

    def update_total_price(self):
        self._total_price = self.get_total_price()

    def apply_percent_discount(self, percent: Decimal) -> None:
        self._total_price = self._total_price * ((100 - percent) / 100)

    def apply_cashback_discount(self, cashback: Decimal) -> None:
        self._customer.add_cashback(self._total_price * (cashback / 100))

    def apply_free_delivery_discount(self) -> None:
        self._free_delivery = True

    def apply_gift_discount(self, gift: Product) -> None:
        self.add_item(gift)