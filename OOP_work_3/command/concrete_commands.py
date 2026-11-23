from command import Command


class AddProductCommand(Command):
    ...


class ChangePriceCommand(Command):
    ...


class ChangeQuantityCommand(Command):
    ...


class MoveProductCommand(Command):
    ...


class RemoveProductCommand(Command):
    ...


class CreateOrderCommand(Command):
    ...


class CancelOrderCommand(Command):
    ...


class ConfirmPaymentCommand(Command):
    ...


class ShipOrderCommand(Command):
    ...


class ShowStatisticsCommand(Command):
    ...


class ShowProductsCommand(Command):
    ...


class ShowOrdersCommand(Command):
    ...