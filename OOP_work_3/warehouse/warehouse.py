from product.product import Product, Price
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
            raise ValueError("Warehouse size must be greater than zero")
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
        if id < 1:
            raise ValueError("Product ID can't be less than 1")
        for index, product in enumerate(self._products):
            if product.id == id:
                del self._products[index]
                self._current_size -= 1
                product._warehouse = None
                return True
        return False

    def remove_by_index(self, index: int) -> bool:
        if 0 <= index < len(self._products):
            product = self._products[index]
            del self._products[index]
            self._current_size -= 1
            product._warehouse = None
            return True
        else:
            raise IndexError("Index out of range")

    def find_by_id(self, product_id: int) -> Product | None:
        if product_id < 1:
            raise ValueError("Product ID doesn't exist")
        for product in self._products:
            if product.id == product_id:
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

    def change_price(self, product_id: int, new_price: str) -> None:
        product = self.find_by_id(product_id)
        if product is None:
            raise ValueError(f"Product with ID {product_id} wasn't found in the warehouse")
        product.set_price(Price(new_price))

    def change_quantity(self, product_id: int, delta: int) -> None:
        product = self.find_by_id(product_id)
        if product is None:
            raise ValueError(f"Product with ID {product_id} wasn't found in the warehouse")
        product.change_quantity(delta)

    def remove_product(self, product_id: int) -> None:
        product = self.find_by_id(product_id)
        if product is None:
            raise ValueError(f"Product with ID {product_id} wasn't found in the warehouse")
        self.remove_by_id(product_id)

    def move_product(self, product_id: int, other_warehouse: "Warehouse") -> None:
        product = self.find_by_id(product_id)
        if product is None:
            raise ValueError(f"Product with ID {product_id} wasn't found in the warehouse")
        product.transfer_to(other_warehouse)

    def short_info(self) -> str:
        if len(self._products) == 0:
            return "Warehouse is empty."
        lines = []
        for product in self._products:
            lines.append(product.short_info())
        return "\n".join(lines)