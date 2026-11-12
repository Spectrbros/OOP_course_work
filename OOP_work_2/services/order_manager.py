from decimal import Decimal
from customer.customer import Customer
from product.product import Product
from order.order import Order

class OrderManager:
    def __init__(self, customer_max_active_orders: int = 5, max_active_orders: int = 100):
        self._orders: dict[int, Order] = {}
        self._customers: dict[int, Customer] = {}
        self._customer_active_orders: dict[Customer, int] = {}
        self._turnover = Decimal("0")
        self._customer_max_active_orders = customer_max_active_orders
        self._max_active_orders = max_active_orders


    def create_order(self, customer: Customer, items: list[Product]) -> None:
        order = Order(customer, items)
        self._orders[order.id] = order
        self._customers[customer.id] = customer
        self._customer_active_orders[]

    def active_orders_count(self):
        return self._active_orders

    @active_orders.setter
    def active_orders(self, delta: int):
        new_value = self._active_orders + delta
        if new_value< 0:
            raise ValueError(f"Active orders count can't be negative: {self._active_orders} + ({delta}) = {new_value}")
        self._active_orders = new_value

    def update_status(self):
        ...
    def get_turnover(self):
        ...
    def get_customer_count(self):
        ...