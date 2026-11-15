from decimal import Decimal
from datetime import datetime

from observer.i_observable import IObservable
from observer.i_observer import IObserver
from observer.order_event import OrderEvent
from order.order_status import OrderStatus
from product.product import Product
from discount.discount import Discount
from delivery.delivery import Delivery
from customer.customer import Customer
from logging.logger import Logger
from logging.logging_source import LoggingSource


class Order(IObservable):
    _next_id = 1

    def __init__(self, customer: Customer, region: str) -> None:
        if region == "":
            raise ValueError("")
        self._id = Order._next_id
        Order._next_id += 1
        self._customer = customer
        self._region = region
        self._items = []
        self._status = OrderStatus.PENDING
        self._delivery = None
        self._free_delivery = False
        self._discounts = []
        self._total_price = Decimal("0")
        self._observers = []
        self._created_at = datetime.now()
        self._logger = Logger()

    def __add__(self, discount: Discount) -> "Order":
        self.apply_discount(discount)
        return self

    def __str__(self) -> str:
        order_id = self._id
        order_status = self._status
        customer_id = self._customer.id
        order_items = ", ".join([f"{i.type.category} x {i.quantity}" for i in self._items])
        order_delivery = self._delivery.name if self._delivery is not None else "Not assigned"
        order_delivery_cost = self.delivery_cost
        free_delivery = str(self._free_delivery)
        order_discounts = ", ".join([f"{i.name}" for i in self._discounts])
        total_price = self._total_price

        info = (f"Order ID: {order_id} | "
                f"Status: {order_status} | "
                f"Customer: {customer_id} | "
                f"Items: {order_items} | "
                f"Delivery: {order_delivery} ({order_delivery_cost:.2f} ₽) | "
                f"Free delivery: {free_delivery} | "
                f"Discounts: {order_discounts} | "
                f"Total price: {total_price}")

        return info

    @property
    def id(self) -> int:
        return self._id

    @property
    def customer(self) -> Customer:
        return self._customer

    @property
    def region(self):
        return self._region

    @property
    def delivery_cost(self) -> Decimal:
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

    def update_total_price(self) -> None:
        self._total_price = self.total_price

    def subscribe(self, observer: IObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def unsubscribe(self, observer: IObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event: OrderEvent) -> None:
        for observer in tuple(self._observers):
            observer.on_order_event(event)

    def set_status(self, new_status: OrderStatus) -> None:
        if not isinstance(new_status, OrderStatus):
            raise TypeError("The status must be set to OrderStatus")
        if new_status == self._status:
            return
        if not self._status.can_transition_to(new_status):
            raise ValueError(f"Invalid status transition: {self._status.value} -> {new_status.value}")
        old_status = self._status
        self._status = new_status
        self._logger.log(LoggingSource.ORDER,f"Order #{self._id}: status {old_status.value} -> {new_status.value}")
        event = OrderEvent(self._id, old_status, new_status, datetime.now())
        self.notify(event)

    def add_item(self, item: Product) -> None:
        self._items.append(item)
        self.update_total_price()
        self._logger.log(LoggingSource.ORDER,f"Item added to order #{self._id}: {item.type.category} x{item.quantity}")

    def remove_item(self, id: int) -> None:
        if id < 1:
            raise ValueError("Product ID doesn't exist")
        for index, item in enumerate(self._items):
            if item.id == id:
                del self._items[index]
                self.update_total_price()
                self._logger.log(LoggingSource.ORDER,f"Item #{id} has been removed from order #{self._id}")
                return
        raise ValueError("There is no product with this ID in the order.")

    def get_items(self) -> tuple:
        return tuple(self._items)

    def set_delivery(self, delivery: Delivery) -> None:
        self._delivery = delivery
        self.update_total_price()
        self._logger.log(LoggingSource.ORDER,f"Delivery assigned to order #{self._id}: {delivery.name}")

    def apply_discount(self, discount: Discount) -> None:
        if any(isinstance(i, type(discount)) for i in self._discounts):
            raise ValueError("An order can't have more than one discount of the same type.")
        self._discounts.append(discount)
        discount.apply(self)
        self.update_total_price()
        self._logger.log(LoggingSource.ORDER, f"A discount has been applied to order #{self._id}: {discount.name}")

    def apply_percent_discount(self, amount: Decimal) -> None:
        self._total_price -= amount

    def apply_cashback_discount(self, amount: Decimal) -> None:
        self._customer.add_cashback(amount)

    def apply_free_delivery_discount(self) -> None:
        self._free_delivery = True

    def apply_gift_discount(self, gift: Product) -> None:
        self.add_item(gift)