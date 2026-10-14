from products import *
class Warehouse:
    def __init__(self, max_size: int):
        if max_size < 0:
            raise ValueError("Size can't be negative")
        self._products = list()
        self._max_size = max_size
        self._current_size = 0

    def add_product(self, product: Product):
        ...

    def remove_by_id(self, id: int):
        ...

    def remove_by_index(self, index: int):
        ...

    def find_by_id(self, id: int) -> Product:
        ...

    def find_by_category(self, category: str) -> list:
        ...

    def find_by_price(self, price: Price) -> list:
        ...