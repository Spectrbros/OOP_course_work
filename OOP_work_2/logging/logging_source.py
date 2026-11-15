from enum import Enum


class LoggingSource(Enum):
    ORDER = "ORDER"
    DELIVERY = "DELIVERY"
    DISCOUNT = "DISCOUNT"
    MANAGER = "MANAGER"