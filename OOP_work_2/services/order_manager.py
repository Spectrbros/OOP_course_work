from decimal import Decimal

from observer.i_observer import IObserver
from observer.order_event import OrderEvent
from customer.customer import Customer
from product.product import Product
from order.order import Order
from order.order_status import OrderStatus


class OrderManager(IObserver):
    def __init__(self, customer_max_active_orders: int = 5, max_active_orders: int = 100) -> None:
        self._orders: dict[int, Order] = {}
        self._customers: dict[int, Customer] = {}
        self._customer_active_orders: dict[Customer, set[Order]] = {}
        self._turnover = Decimal("0")
        self._active_orders_count = 0
        self._CUSTOMER_MAX_ACTIVE_ORDERS = customer_max_active_orders
        self._MAX_ACTIVE_ORDERS = max_active_orders

    def on_order_event(self, event: OrderEvent) -> None:
        order = self.get_order(event.order_id)
        if OrderEvent.new_status is OrderStatus.PAID:
            self._turnover += order.total_price
        if (OrderEvent.old_status is OrderStatus.PAID and
            OrderEvent.new_status is OrderStatus.CANCELLED
        ):
            self._turnover -= order.total_price
        if (event.old_status.is_active() and not
            event.new_status.is_active()
        ):
            customer = order.customer
            self._customer_active_orders[customer].remove(order)
            self._active_orders_count -= 1


    def create_order(self, customer: Customer, items: list[Product]) -> None:
        if customer.id in self._customers and self.get_customer_active_orders_count(customer) > self._CUSTOMER_MAX_ACTIVE_ORDERS:
            raise ValueError("Customer has the maximum number of active orders")
        if len(items) == 0:
            raise ValueError("List of items can't be empty")
        order = Order(customer)
        for item in items:
            order.add_item(item)
        self._orders[order.id] = order
        order.subscribe(self)
        if customer.id not in self._customers:
            self._customers[customer.id] = customer
            self._customer_active_orders[customer] = set()
        self._customer_active_orders[customer].add(order)
        self._active_orders_count += 1

    @property
    def active_orders_count(self) -> int:
        return self._active_orders_count

    def get_customer_active_orders_count(self, customer: Customer) -> int:
        return len(self._customer_active_orders[customer])

    def get_order(self, order_id: int) -> Order:
        if order_id not in self._orders:
            raise KeyError(f"Order #{order_id} not found")
        return self._orders[order_id]

    def update_status(self, order_id: int, new_status: OrderStatus) -> None:
        order = self.get_order(order_id)
        order.set_status(new_status)

    @property
    def turnover(self) -> Decimal:
        return self._turnover

    @property
    def customer_count(self) -> int:
        return len(self._customers)