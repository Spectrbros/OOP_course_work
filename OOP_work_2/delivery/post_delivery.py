from delivery import Delivery
from order import Order

class PostDelivery(Delivery):
    def get_cost(self, order: Order):
        ...

    def get_estimated_time(self):
        ...

    def is_available(self, order: Order):
        ...