from decimal import Decimal

from observer.i_observer import IObserver
from observer.order_event import OrderEvent
from customer.customer import Customer
from product.product import Product
from order.order import Order
from order.order_status import OrderStatus
from delivery.delivery_region import DeliveryRegion
from logging_service.logger import Logger
from logging_service.logging_source import LoggingSource


class OrderManager(IObserver):
    def __init__(self, customer_max_active_orders: int = 5, max_active_orders: int = 100) -> None:
        if customer_max_active_orders < 1:
            raise ValueError("The maximum count of active customer orders can't be less than 1")
        if max_active_orders < 1:
            raise ValueError("The maximum count of active orders can't be less than 1")
        self._orders: dict[int, Order] = {}
        self._customers: dict[int, Customer] = {}
        self._customer_active_orders: dict[int, set[int]] = {}
        self._turnover = Decimal("0")
        self._active_orders_count = 0
        self._CUSTOMER_MAX_ACTIVE_ORDERS = customer_max_active_orders
        self._MAX_ACTIVE_ORDERS = max_active_orders
        self._logger = Logger()

    @property
    def active_orders_count(self) -> int:
        return self._active_orders_count

    @property
    def turnover(self) -> Decimal:
        return self._turnover

    @property
    def customer_count(self) -> int:
        return len(self._customers)

    @property
    def orders_count(self) -> int:
        return len(self._orders)

    @property
    def customer_max_active_orders(self) -> int:
        return self._CUSTOMER_MAX_ACTIVE_ORDERS

    @property
    def max_active_orders(self) -> int:
        return self._MAX_ACTIVE_ORDERS

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
            self._customer_active_orders[customer.id].discard(order.id)
            self._active_orders_count -= 1
        self._logger.log(
            LoggingSource.MANAGER,
            f"Order #{order.id}: "
            f"{event.old_status.value} -> {event.new_status.value}; "
            f"turnover: {self._turnover:.2f} RUB; "
            f"active orders: {self.active_orders_count}; "
            f"customers: {self.customer_count}",
        )

    def check_limits(self, customer: Customer) -> None:
        if self._active_orders_count >= self._MAX_ACTIVE_ORDERS:
            self._logger.log(LoggingSource.MANAGER,f"Order creation rejected: the manager limit of active orders has been reached")
            raise ValueError("Manager has the maximum number of active orders")
        if customer.id in self._customers and self.get_customer_active_orders_count(customer) >= self._CUSTOMER_MAX_ACTIVE_ORDERS:
            self._logger.log(LoggingSource.MANAGER,f"Order creation for customer #{customer.id} rejected: the limit of {self._CUSTOMER_MAX_ACTIVE_ORDERS} active orders has been reached")
            raise ValueError("Customer has the maximum number of active orders")

    def create_order(self, customer: Customer, region: DeliveryRegion, items: list[Product], quantities: list[int] | None = None) -> Order:
        self.check_limits(customer)
        if len(items) == 0:
            self._logger.log(LoggingSource.MANAGER,f"Order creation for customer #{customer.id} rejected: the list of items is empty")
            raise ValueError("List of items can't be empty")
        if quantities is None:
            quantities = [item.quantity for item in items]
        if len(quantities) != len(items):
            raise ValueError("Quantities count must match items count")
        order = Order(customer, region)
        for item, quantity in zip(items, quantities):
            order.add_item(item, quantity)
        self._orders[order.id] = order
        order.subscribe(self)
        if customer.id not in self._customers:
            self._customers[customer.id] = customer
            self._customer_active_orders[customer.id] = set()
        self._customer_active_orders[customer.id].add(order.id)
        self._active_orders_count += 1
        self._logger.log(LoggingSource.MANAGER,f"Order #{order.id} has been created for customer #{customer.id}")
        return order

    def cancel_order(self, order_id: int) -> None:
        order = self.get_order(order_id)
        if not order.status.can_transition_to(OrderStatus.CANCELLED):
            raise ValueError(f"Order #{order.id} cannot be cancelled from status {order.status.value}")
        order.set_status(OrderStatus.CANCELLED)

    def confirm_payment(self, order_id: int) -> None:
        order = self.get_order(order_id)
        if order.status != OrderStatus.PENDING:
            raise ValueError("Only an order in Pending status can be paid")
        order.set_status(OrderStatus.PAID)

    def ship_order(self, order_id: int) -> None:
        order = self.get_order(order_id)
        if order.status != OrderStatus.PAID:
            raise ValueError("Only a paid order can be shipped")
        order.set_status(OrderStatus.SHIPPED)

    def get_customer_active_orders_count(self, customer: Customer) -> int:
        if customer.id not in self._customer_active_orders:
            raise KeyError("Customer is not yet registered in the order manager and has no orders.")
        return len(self._customer_active_orders[customer.id])

    def get_order(self, order_id: int) -> Order:
        if order_id not in self._orders:
            raise KeyError(f"Order #{order_id} not found")
        return self._orders[order_id]

    def update_status(self, order_id: int, new_status: OrderStatus) -> None:
        order = self.get_order(order_id)
        order.set_status(new_status)

    def list_orders(self) -> str:
        if len(self._orders) == 0:
            return "There are no orders."
        lines = []
        for order in self._orders.values():
            if order.status.is_active():
                mark = "[active]"
            else:
                mark = "[finished]"
            lines.append(f"{mark} {order}")
        return "\n".join(lines)

    def get_statistics(self) -> dict:
        return {
            "orders": len(self._orders),
            "active_orders": self._active_orders_count,
            "turnover": self._turnover,
            "customers": len(self._customers),
        }