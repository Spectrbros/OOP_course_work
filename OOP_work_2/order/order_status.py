from __future__ import annotations

from enum import Enum


class OrderStatus(Enum):
    PENDING = "Pending"
    PAID = "Paid"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"

    _TRANSITIONS = {
        PENDING: {PAID, CANCELLED},
        PAID: {SHIPPED, CANCELLED},
        SHIPPED: {DELIVERED},
        DELIVERED: set(),
        CANCELLED: set()
    }

    def can_transition_to(self, new_status: OrderStatus) -> bool:
        return new_status in self._TRANSITIONS[self]

    def is_active(self) -> bool:
        return self in (OrderStatus.PENDING, OrderStatus.PAID, OrderStatus.SHIPPED)
