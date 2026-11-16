from __future__ import annotations

from enum import Enum


class ProductCategory(Enum):
    MUG = ("mug", 0.3, "300")
    FRYING_PAN = ("frying pan", 1.4, "1600")
    PACK_OF_TEA = ("pack of tea", 0.15, "100")
    BOX_OF_CHOCOLATES = ("box of chocolates", 0.8, "700")
    BOTTLE_OF_WATER = ("bottle of water", 1.0, "70")
    HEADPHONES = ("headphones", 0.25, "2500")
    LAPTOP = ("laptop", 2.0, "55000")
    POWERBANK = ("powerbank", 0.4, "1800")
    T_SHIRT = ("t-shirt", 0.2, "900")
    WINTER_JACKET = ("winter jacket", 1.6, "4500")
    BOOK = ("book", 0.6, "550")
    DESK_LAMP = ("desk lamp", 1.2, "1500")
    DUMBBELL = ("dumbbell", 5.0, "900")
    SPORTS_KETTLEBELL = ("sports kettlebell", 15.0, "2000")
    BARBELL = ("barbell", 25.0, "5000")

    def __init__(self, title: str, base_weight: float, base_price: str) -> None:
        self.title = title
        self.base_weight = base_weight
        self.base_price = base_price