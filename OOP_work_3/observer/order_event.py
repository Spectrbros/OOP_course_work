from dataclasses import dataclass
from datetime import datetime

from order.order_status import OrderStatus


@dataclass(frozen=True)
class OrderEvent:
    order_id: int
    old_status: OrderStatus
    new_status: OrderStatus
    timestamp: datetime