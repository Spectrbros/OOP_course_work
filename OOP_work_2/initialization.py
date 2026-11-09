from product.product_type import BaseWeight, BasePrice, ProductType


def catalog_initialization():
    ProductType.register_type("mug", BaseWeight(0.3), BasePrice("300"))
    ProductType.register_type("frying pan", BaseWeight(1.4), BasePrice("1600"))
    ProductType.register_type("pack of tea", BaseWeight(0.15), BasePrice("100"))
    ProductType.register_type("box of chocolates", BaseWeight(0.8), BasePrice("700"))
    ProductType.register_type("bottle of water", BaseWeight(1.0), BasePrice("70"))
    ProductType.register_type("headphones", BaseWeight(0.25), BasePrice("2500"))
    ProductType.register_type("laptop", BaseWeight(2.0), BasePrice("55000"))
    ProductType.register_type("powerbank", BaseWeight(0.4), BasePrice("1800"))
    ProductType.register_type("t-shirt", BaseWeight(0.2), BasePrice("900"))
    ProductType.register_type("winter jacket", BaseWeight(1.6), BasePrice("4500"))
    ProductType.register_type("book", BaseWeight(0.6), BasePrice("550"))
    ProductType.register_type("desk lamp", BaseWeight(1.2), BasePrice("1500"))
    ProductType.register_type("dumbbell", BaseWeight(5.0), BasePrice("900"))
    ProductType.register_type("sports kettlebell", BaseWeight(15.0), BasePrice("2000"))
    ProductType.register_type("barbell", BaseWeight(25.0), BasePrice("5000"))
