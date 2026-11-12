from decimal import Decimal

from customer import customer
from order.order_status import OrderStatus
from product.product import Product
from discount.discount import Discount
from delivery.delivery import Delivery
from customer.customer import Customer


class Order:
    _next_id = 1

    def __init__(self, customer: Customer, items: list[Product]) -> None:
        if len(items) == 0:
            raise ValueError("List of items can't be empty")
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

    def __str__(self) -> str:
        order_id = self._id
        order_status = self._status
        customer_name = self._customer.name
        order_items = ", ".join([f"{i.type.category} x {i.quantity}" for i in self._items])
        order_delivery = self._delivery.name if self._delivery is not None else "Not assigned"
        order_delivery_cost = self.delivery_cost
        free_delivery = str(self._free_delivery)
        order_discounts = ", ".join([f"{i.name}" for i in self._discounts])
        total_price = self._total_price

        info = (f"Order ID: {order_id}\n"
                f"Status: {order_status}\n"
                f"Customer: {customer_name}\n"
                f"Items: {order_items}\n"
                f"Delivery: {order_delivery} | {order_delivery_cost:.2f} ₽\n"
                f"Free delivery: {free_delivery}\n"
                f"Discounts: {order_discounts}\n"
                f"Total price: {total_price}\n")

        return info

    @property
    def id(self):
        return self._id

    @property
    def delivery_cost(self):
        if self._free_delivery:
            return Decimal("0")
        delivery_cost = self._delivery.get_cost(self)
        return delivery_cost

    @property
    def total_weight(self) -> float:
        total_weight = 0
        for item in self._items:
            total_weight += item.weight
        return total_weight

    @property
    def total_price(self) -> Decimal:
        total_price = Decimal("0")
        for item in self._items:
            total_price += item.total_price
        if not self._free_delivery and self._delivery is not None:
            total_price += self.delivery_cost
        return total_price

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

    def update_total_price(self) -> None:
        self._total_price = self.get_total_price()

    def apply_percent_discount(self, percent: Decimal) -> None:
        self._total_price = self._total_price * ((100 - percent) / 100)

    def apply_cashback_discount(self, cashback: Decimal) -> None:
        self._customer.add_cashback(self._total_price * (cashback / 100))

    def apply_free_delivery_discount(self) -> None:
        self._free_delivery = True

    def apply_gift_discount(self, gift: Product) -> None:
        self.add_item(gift)