from products import Product, Price
import copy

class Warehouse:
    def __init__(self, max_size: int):
        if max_size < 0:
            raise ValueError("Size can't be negative")
        self._products = []
        self._max_size = max_size
        self._current_size = 0

    def __deepcopy__(self, memo):
        cls = type(self)
        new = cls.__new__(cls)
        memo[id(self)] = new
        new._max_size = self._max_size
        new._products = [p.clone() for p in self._products]
        new._current_size = self._current_size
        return new

# Конструкторы
    # def clone(self):
        # return copy.deepcopy(self)
    @classmethod
    def copy_constructor(cls, other: 'Warehouse') -> 'Warehouse':
        new_warehouse = cls(other._max_size)
        new_warehouse._products = [p.clone() for p in other._products]
        for p in new_warehouse._products:
            p._warehouse = new_warehouse
        return new_warehouse

    # 2. Оператор присваивания копированием (копирует данные в существующий склад)
    def copy_assign(self, other: 'Warehouse'):
        if self is other:
            return
        self._max_size = other._max_size
        self._products = [p.clone() for p in other._products]
        for p in self._products:
            p._warehouse = self

    # 3. Конструктор перемещения (забирает товары у старого склада без копирования)
    @classmethod
    def move_constructor(cls, other: 'Warehouse') -> 'Warehouse':
        new_warehouse = cls(other._max_size)
        new_warehouse._products = other._products
        for p in new_warehouse._products:
            p._warehouse = new_warehouse
        other._products = []
        return new_warehouse

    # 4. Оператор присваивания перемещением (переносит товары в текущий склад)
    def move_assign(self, other: 'Warehouse'):
        if self is other:
            return
        self._max_size = other._max_size
        self._products = other._products
        for p in self._products:
            p._warehouse = self
        other._products = []

    # 5. Деструктор (формальный вызов при удалении объекта)
    def __del__(self):
        pass

# Действия склада
    def add_product(self, product: Product):
        if len(self._products) >= self._max_size:
            raise ValueError("Warehouse is full")
        self._products.append(product)
        product._warehouse = self

    def remove_by_id(self, id: int) -> bool:
        if id > Product._next_id:
            raise ValueError("Product ID doesn't exist")

        for index, product in enumerate(self._products):
            if product.id == id:
                del self._products[index]
                return True
        return False

    def remove_by_index(self, index: int):
        if 0 <= index < len(self._products):
            del self._products[index]
        else:
            raise IndexError("Index out of range")

    def find_by_id(self, id: int) -> Product:
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