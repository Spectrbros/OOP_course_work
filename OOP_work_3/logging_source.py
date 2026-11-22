from enum import Enum


class LoggingSource(Enum):
    ORDER = "ORDER"
    DELIVERY = "DELIVERY"
    DISCOUNT = "DISCOUNT"
    MANAGER = "MANAGER"
    INPUT = "INPUT"
    COMMAND = "COMMAND"
    RESULT = "RESULT"
    MEDIATOR = "MEDIATOR"
    WAREHOUSE = "WAREHOUSE"
    PAYMENT = "PAYMENT"