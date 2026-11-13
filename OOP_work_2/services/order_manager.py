from decimal import Decimal
from customer.customer import Customer
from product.product import Product
from order.order import Order

class OrderManager:
    def __init__(self, customer_max_active_orders: int = 5, max_active_orders: int = 100):
        self._orders: dict[int, Order] = {}
        self._customers: dict[int, Customer] = {}
        self._customer_active_orders: dict[Customer, set[Order]] = {}
        self._turnover = Decimal("0")
        self._active_orders_count = 0
        self._CUSTOMER_MAX_ACTIVE_ORDERS = customer_max_active_orders
        self._MAX_ACTIVE_ORDERS = max_active_orders


    def create_order(self, customer: Customer, items: list[Product]) -> None:
        if customer.id in self._customers and len(self._customer_active_orders[customer]) > self._CUSTOMER_MAX_ACTIVE_ORDERS:
            raise ValueError("Customer has the maximum number of active orders")
        order = Order(customer, items)
        self._orders[order.id] = order
        if customer.id not in self._customers:
            self._customers[customer.id] = customer
            self._customer_active_orders[customer] = set()
        self._customer_active_orders[customer].add(order)
        self.change_active_orders_count(+1)

    @property
    def active_orders_count(self) -> int:
        return self._active_orders_count

    def change_active_orders_count(self, delta: int):
        new_value = self._active_orders_count + delta
        if new_value< 0:
            raise ValueError(f"Active orders count can't be negative: {self._active_orders_count} + ({delta}) = {new_value}")
        self._active_orders_count = new_value

    def update_status(self):
        ...

    @property
    def turnover(self):
        return self._turnover

    @property
    def customer_count(self):
        return len(self._customers)