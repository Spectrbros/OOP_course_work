from decimal import Decimal

from observer.i_observer import IObserver
from observer.order_event import OrderEvent
from customer.customer import Customer
from product.product import Product
from product.catalog import catalog_initialization
from order.order import Order
from order.order_status import OrderStatus
from delivery.delivery_region import DeliveryRegion
from logging.logger import Logger
from logging.logging_source import LoggingSource


class OrderManager(IObserver):
    def __init__(self, customer_max_active_orders: int = 5, max_active_orders: int = 100) -> None:
        if customer_max_active_orders < 1:
            raise ValueError("The maximum count of active customer orders can't be less than 1")
        if max_active_orders < 1:
            raise ValueError("The maximum count of active orders can't be less than 1")
        catalog_initialization()
        self._orders: dict[int, Order] = {}
        self._customers: dict[int, Customer] = {}
        self._customer_active_orders: dict[Customer, set[Order]] = {}
        self._turnover = Decimal("0")
        self._active_orders_count = 0
        self._CUSTOMER_MAX_ACTIVE_ORDERS = customer_max_active_orders
        self._MAX_ACTIVE_ORDERS = max_active_orders
        self._logger = Logger()

    def on_order_event(self, event: OrderEvent) -> None:
        order = self.get_order(event.order_id)
        if event.new_status is OrderStatus.PAID:
            self._turnover += order.total_price
        if (event.old_status is OrderStatus.PAID and
            event.new_status is OrderStatus.CANCELLED
        ):
            self._turnover -= order.total_price
        if (event.old_status.is_active() and not
            event.new_status.is_active()
        ):
            customer = order.customer
            self._customer_active_orders[customer].remove(order)
            self._active_orders_count -= 1
        self._logger.log(
            LoggingSource.MANAGER,
            f"Order #{order.id}: "
            f"{event.old_status.value} -> {event.new_status.value}; "
            f"turnover: {self._turnover:.2f} RUB; "
            f"active orders: {self.active_orders_count}; "
            f"customers: {self.customer_count}",
        )

    def create_order(self, customer: Customer, region: DeliveryRegion, items: list[Product]) -> Order:
        if self._active_orders_count >= self._MAX_ACTIVE_ORDERS:
            self._logger.log(LoggingSource.MANAGER,f"Order creation rejected: the manager limit of active orders has been reached")
            raise ValueError("Manager has the maximum number of active orders")
        if customer.id in self._customers and self.get_customer_active_orders_count(customer) >= self._CUSTOMER_MAX_ACTIVE_ORDERS:
            self._logger.log(LoggingSource.MANAGER,f"Order creation for customer #{customer.id} rejected: the limit of {self._CUSTOMER_MAX_ACTIVE_ORDERS} active orders has been reached")
            raise ValueError("Customer has the maximum number of active orders")
        if len(items) == 0:
            self._logger.log(LoggingSource.MANAGER,f"Order creation for customer #{customer.id} rejected: the list of items is empty")
            raise ValueError("List of items can't be empty")
        order = Order(customer, region)
        for item in items:
            order.add_item(item)
        self._orders[order.id] = order
        order.subscribe(self)
        if customer.id not in self._customers:
            self._customers[customer.id] = customer
            self._customer_active_orders[customer] = set()
        self._customer_active_orders[customer].add(order)
        self._active_orders_count += 1
        self._logger.log(LoggingSource.MANAGER,f"Order #{order.id} has been created for customer #{customer.id}")
        return order

    @property
    def active_orders_count(self) -> int:
        return self._active_orders_count

    @property
    def turnover(self) -> Decimal:
        return self._turnover

    @property
    def customer_count(self) -> int:
        return len(self._customers)

    def get_customer_active_orders_count(self, customer: Customer) -> int:
        if customer not in self._customer_active_orders:
            raise KeyError("Customer is not yet registered in the order manager and has no orders.")
        return len(self._customer_active_orders[customer])

    def get_order(self, order_id: int) -> Order:
        if order_id not in self._orders:
            raise KeyError(f"Order #{order_id} not found")
        return self._orders[order_id]

    def update_status(self, order_id: int, new_status: OrderStatus) -> None:
        order = self.get_order(order_id)
        order.set_status(new_status)