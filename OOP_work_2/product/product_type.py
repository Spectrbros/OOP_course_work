class ProductType:
    _pool = {}

    def __init__(self):
        self._category = 0
        self._base_weight = 0
        self._base_price = 0