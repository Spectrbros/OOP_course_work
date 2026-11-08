from delivery import Delivery
from order.order import Order

class CourierDelivery(Delivery):
    def get_cost(self, order: Order):
        ...

    def get_estimated_time(self):
        ...

    def is_available(self, order: Order):
        ...