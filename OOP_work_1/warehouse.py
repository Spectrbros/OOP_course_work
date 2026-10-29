from products import Product, Price
import copy

class WarehouseIterator:
    def __init__(self, products):
        self._products = products
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._products):
            raise StopIteration
        product = self._products[self._index]
        self._index += 1
        return product

class Warehouse:
    def __init__(self, max_size: int):
        if max_size <= 0:
            raise ValueError("Size can't be negative")
        self._products = []
        self._max_size = max_size
        self._current_size = 0

    def __deepcopy__(self, memo):
        cls = type(self)
        new = cls.__new__(cls)
        memo[id(self)] = new
        new._max_size = self._max_size
        new._current_size = self._current_size
        new._products = [product.clone() for product in self._products]
        for product in new._products:
            product._warehouse = new
        return new

    def __iter__(self):
        return WarehouseIterator(self._products)

    def copy(self) -> 'Warehouse':
        return copy.deepcopy(self)

    def copy_from(self, other: 'Warehouse') -> None:
        if other is self:
            raise ValueError("Cannot copy warehouse into itself")
        if other._current_size > self._max_size:
            raise ValueError("Source warehouse exceeds this warehouse capacity")

        new_products = [product.clone() for product in other._products]
        for product in new_products:
            product._warehouse = self

        self._products = new_products
        self._current_size = other._current_size

    def move_from(self, other: 'Warehouse') -> None:
        if other is self:
            raise ValueError("Cannot move warehouse into itself")
        if other._current_size > self._max_size:
            raise ValueError("Source warehouse exceeds this warehouse capacity")

        self._products = other._products
        self._current_size = other._current_size
        for product in self._products:
            product._warehouse = self

        other._products = []
        other._current_size = 0

    @classmethod
    def moved_from(cls, other: 'Warehouse') -> 'Warehouse':
        new_warehouse = cls(other._max_size)
        new_warehouse.move_from(other)
        return new_warehouse

    # 5. Деструктор (не нужен)
    def __del__(self):
        pass

# Действия склада
    @property
    def size(self) -> int:
        return  self._current_size

    @property
    def max_size(self) -> int:
        return self._max_size

    @property
    def products(self) -> list:
        return self._products

    def add_product(self, product: Product):
        if self._current_size >= self._max_size:
            raise ValueError("Warehouse is full")
        self._products.append(product)
        product._warehouse = self
        self._current_size += 1

    def remove_by_id(self, id: int) -> bool:
        if id > Product._next_id or id < 1:
            raise ValueError("Product ID doesn't exist")
        for index, product in enumerate(self._products):
            if product.id == id:
                del self._products[index]
                self._current_size -= 1
                return True
        return False

    def remove_by_index(self, index: int):
        if 0 <= index < len(self._products):
            del self._products[index]
            self._current_size -= 1
        else:
            raise IndexError("Index out of range")

    def find_by_id(self, id: int) -> Product:
        if id < 1:
            raise ValueError("Product ID doesn't exist")
        for product in self._products:
            if product.id == id:
                return product
        return None

    def find_by_category(self, category: str) -> list:
        one_category_list = []
        for product in self._products:
            if product.category == category:
                one_category_list.append(product)
        return one_category_list

    def find_by_price(self, price: Price) -> list:
        one_price_list = []
        for product in self._products:
            if product.price.value == price.value:
                one_price_list.append(product)
        return one_price_list