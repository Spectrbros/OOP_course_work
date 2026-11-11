class OrderManager:
    def __init__(self):
        self._orders: dict[int, tuple] = {}
        self._customers = set()
        self._turnover = 0
        self._max_active_orders = 0

    def create_order(self):
        ...
    def update_status(self):
        ...
    def get_turnover(self):
        ...
    def get_customer_count(self):
        ...