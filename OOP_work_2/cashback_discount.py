from discount import Discount
from order import Order

class CashbackDiscount(Discount):
    def apply(self, order: Order):
        ...