class OrderManager:
    def __init__(self):
        self._orders = 0
        self._customers = 0
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