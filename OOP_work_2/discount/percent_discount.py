from discount import Discount
from order import Order

class PercentDiscount(Discount):
    def apply(self, order: Order):
        ...