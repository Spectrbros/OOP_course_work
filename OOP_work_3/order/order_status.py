from __future__ import annotations

from enum import Enum


class OrderStatus(Enum):
    PENDING = "Pending"
    PAID = "Paid"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"

    def can_transition_to(self, new_status: OrderStatus) -> bool:
        return new_status in _TRANSITIONS[self]

    def is_active(self) -> bool:
        return self in (OrderStatus.PENDING, OrderStatus.PAID, OrderStatus.SHIPPED)

_TRANSITIONS = {
    OrderStatus.PENDING: {OrderStatus.PAID, OrderStatus.CANCELLED},
    OrderStatus.PAID: {OrderStatus.SHIPPED, OrderStatus.CANCELLED},
    OrderStatus.SHIPPED: {OrderStatus.DELIVERED},
    OrderStatus.DELIVERED: set(),
    OrderStatus.CANCELLED: set()
}