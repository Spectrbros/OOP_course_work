from discount import Discount
from order import Order

class GiftDiscount(Discount):
    def apply(self, order: Order):
        ...