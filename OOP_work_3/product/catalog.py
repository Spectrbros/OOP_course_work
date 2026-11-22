from product.product_category import ProductCategory
from product.product_type import BaseWeight, BasePrice, ProductType

_initialized = False


def catalog_initialization() -> None:
    global _initialized
    if _initialized:
        return
    for category in ProductCategory:
        ProductType.register_type(category.title, BaseWeight(category.base_weight), BasePrice(category.base_price))
    _initialized = True