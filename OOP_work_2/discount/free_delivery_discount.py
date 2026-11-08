from discount import Discount
from order import Order

class FreeDeliveryDiscount(Discount):
    def apply(self, order: Order):
        ...