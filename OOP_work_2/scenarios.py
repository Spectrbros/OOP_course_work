from manager.order_manager import OrderManager
from customer.customer import Customer
from delivery.delivery_region import DeliveryRegion
from product.product import Product
from product.product_category import ProductCategory
from discount.percent_discount import PercentDiscount
from discount.free_delivery_discount import FreeDeliveryDiscount
from discount.cashback_discount import CashbackDiscount
from discount.gift_discount import GiftDiscount
from delivery.delivery_proxy import DeliveryProxy
from delivery.courier_delivery import CourierDelivery
from order.order_status import OrderStatus

def scenario_1() -> None:
    print("=== Сценарий 1: создание заказа, добавление товаров и применение процентной скидки ===")
    manager = OrderManager(5, 100)
    customer = Customer("Ivan", 26, 79301234567, "ivan@mail.ru")
    order = manager.create_order(customer, DeliveryRegion.SAINT_PETERSBURG,[Product.from_category(ProductCategory.MUG, 3)])
    print(f"\n{order}\n")
    order.add_item(Product.from_category(ProductCategory.POWERBANK, 1))
    print(f"\n{order}\n")
    order.add_item(Product.from_category(ProductCategory.BOOK, 2))
    print(f"\n{order}\n")
    order = order + PercentDiscount("10")
    print(f"\n{order}\n")
    print()

def scenario_2() -> None:
    print("=== Сценарий 2: выбор способа доставки и проверка доступности через DeliveryProxy ===")
    manager = OrderManager(5, 100)
    customer = Customer("Petr", 30, 79111234567, "petr@mail.ru")
    order = manager.create_order(customer, DeliveryRegion.MOSCOW,[Product.from_category(ProductCategory.HEADPHONES, 1)])
    print(f"\n{order}\n")

    print("- Order weighing 0.25 kg: courier available -")
    proxy = DeliveryProxy(CourierDelivery())
    print(f"Courier available: {proxy.is_available(order)}")
    print(f"Delivery cost: {proxy.get_cost(order)} RUB")
    print(f"Estimated delivery time: {proxy.get_estimated_time(order)}")
    proxy << order
    print(f"\n{order}\n")

    print("- Order weighing 25 kg: courier unavailable -")
    heavy_order = manager.create_order(customer,DeliveryRegion.MOSCOW,[Product.from_category(ProductCategory.BARBELL, 1)])
    heavy_proxy = DeliveryProxy(CourierDelivery())
    print(f"Order weight: {heavy_order.total_weight} kg")
    print(f"Proxy available: {heavy_proxy.is_available(heavy_order)}")
    print(f"Cost (selected method): {heavy_proxy.get_cost(heavy_order)} RUB")
    print(f"Estimated time (selected method): {heavy_proxy.get_estimated_time(heavy_order)}")
    heavy_proxy << heavy_order
    print(f"\n{heavy_order}\n")
    print()

def scenario_3() -> None:
    print("=== Сценарий 3: смена статуса заказа, уведомление OrderManager, обновление оборота ===")
    manager = OrderManager(5, 100)
    customer = Customer("Anna", 28, 79221234567, "anna@mail.ru")
    order = manager.create_order(customer,DeliveryRegion.KAZAN,[Product.from_category(ProductCategory.MUG, 2)])
    print(f"Turnover before payment: {manager.turnover} RUB; active orders: {manager.active_orders_count}\n")

    manager.update_status(order.id, OrderStatus.PAID)
    print(f"Turnover after payment (Pending -> Paid): {manager.turnover} RUB\n")

    manager.update_status(order.id, OrderStatus.SHIPPED)
    manager.update_status(order.id, OrderStatus.DELIVERED)
    print(f"Turnover after delivery (Paid -> Shipped -> Delivered): {manager.turnover} RUB")
    print(f"Active orders after delivery: {manager.active_orders_count}\n")

    print(f"{order}\n")
    print()

def scenario_4() -> None:
    print("=== Сценарий 4: применение нескольких скидок к одному заказу, проверка итоговой цены ===")
    manager = OrderManager(5, 100)
    customer = Customer("Olga", 35, 79331234567, "olga@mail.ru")
    order = manager.create_order(
        customer, DeliveryRegion.YEKATERINBURG,
        [Product.from_category(ProductCategory.MUG, 2),
            Product.from_category(ProductCategory.BOOK, 1),]
    )
    CourierDelivery() << order
    print(f"\nTotal including courier delivery: {order.total_price} RUB\n")

    order = order + PercentDiscount("10")
    print(f"After a 10% discount: {order.total_price} RUB\n")

    order = order + CashbackDiscount("5")
    print(f"After 5% cashback: {order.total_price} RUB\n")

    order = order + FreeDeliveryDiscount()
    print(f"After free delivery: {order.total_price} RUB\n")

    order = order + GiftDiscount()
    print(f"After a gift: {order.total_price} RUB\n")

    print(f"{order}\n")
    print()

def scenario_5() -> None:
    print("=== Сценарий 5: отмена заказа, освобождение лимита активных заказов, обновление статистики клиентов ===")
    manager = OrderManager(2, 100)
    customer = Customer("Vladimir", 40, 79441234567, "vladimir@mail.ru")

    first_order = manager.create_order(customer, DeliveryRegion.MOSCOW, [Product.from_category(ProductCategory.LAPTOP, 1)])
    second_order = manager.create_order(customer,DeliveryRegion.MOSCOW,[Product.from_category(ProductCategory.SPORTS_KETTLEBELL, 2)])
    print(f"Active orders created: {manager.active_orders_count}; customers: {manager.customer_count}\n")

    try:
        manager.create_order(customer, DeliveryRegion.MOSCOW, [Product.from_category(ProductCategory.T_SHIRT, 1)])
    except ValueError as error:
        print(f"Limit of 2 active orders per client reached: {error}\n")

    manager.update_status(second_order.id, OrderStatus.CANCELLED)
    print(f"After canceling order #{second_order.id}: active orders {manager.active_orders_count}\n")

    third_order = manager.create_order(customer, DeliveryRegion.MOSCOW,[Product.from_category(ProductCategory.T_SHIRT, 1)])
    print(f"After freeing up the limit, order #{third_order.id} was created: active orders {manager.active_orders_count}\n")

    manager.update_status(first_order.id, OrderStatus.PAID)
    print(f"Turnover: {manager.turnover} RUB;\n"
          f"active orders: {manager.active_orders_count};\n"
          f"customers: {manager.customer_count}\n")
    print()

def run_all_scenarios() -> None:
    scenario_1()
    scenario_2()
    scenario_3()
    scenario_4()
    scenario_5()