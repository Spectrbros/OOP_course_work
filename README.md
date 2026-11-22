# Лабораторные работы по дисциплине «Объектно-ориентированное программирование»

## Содержание

1. [Работа 1 — Введение в ООП: классы, наследование, контейнеры](#work-1)
2. [Работа 2 — Интерфейсы классов, взаимодействие классов, перегрузка операций](#work-2)

---

<a id="work-1"></a>
## Работа 1 — Введение в ООП: классы, наследование, контейнеры

**Система:** управление складом и каталогом товаров.

- Иерархия товаров: `Product` → `Electronics` / `Clothing` / `Food` → конкретные товары
  (`Smartphone`, `Laptop`, `TShirt`, `Jacket`, `Milk`, `Bread`).
- Классы-атрибуты `Price`, `Quantity`, `Weight` с проверкой корректности значений.
- `Warehouse` — контейнер с ограничением вместимости; `WarehouseIterator` — обход товаров.
- Паттерны: **Фабричный метод / Абстрактная фабрика** (`ProductFactory` + 6 конкретных фабрик),
  **Итератор** (`WarehouseIterator`).
- Глубокое копирование (`copy` / `__deepcopy__`) и перемещение (`move_from`) склада.
- Поиск по ID / категории / цене, удаление по ID / индексу, перенос товара между складами.
- 5 демонстрационных сценариев.

### UML-диаграмма классов

```mermaid
classDiagram
    class Price {
        -value
        +value
    }
    class Quantity {
        -value
        +value
        +change(delta)
    }
    class Weight {
        -value
        +value
    }
    class Product {
        <<abstract>>
        -id
        -name
        -category
        -price
        -quantity
        -weight
        -warehouse
        +clone()*
        +change_quantity(delta)
        +set_price(price)
        +transfer_to(other)
        +info()
    }
    class Electronics {
        <<abstract>>
    }
    class Clothing {
        <<abstract>>
    }
    class Food {
        <<abstract>>
    }
    class Smartphone
    class Laptop
    class TShirt
    class Jacket
    class Milk
    class Bread
    class ProductFactory {
        <<abstract>>
        +create_product(name, price, quantity, weight)*
    }
    class SmartphoneFactory
    class LaptopFactory
    class TShirtFactory
    class JacketFactory
    class MilkFactory
    class BreadFactory
    class Warehouse {
        -products
        -max_size
        -current_size
        +size
        +max_size
        +products
        +copy()
        +copy_from(other)
        +move_from(other)
        +moved_from(other)$
        +add_product(product)
        +remove_by_id(id)
        +remove_by_index(index)
        +find_by_id(id)
        +find_by_category(category)
        +find_by_price(price)
    }
    class WarehouseIterator {
        -products
        -index
        +__iter__()
        +__next__()
    }

    Product *-- Price
    Product *-- Quantity
    Product *-- Weight
    Product --> Warehouse : located on

    Product <|-- Electronics
    Product <|-- Clothing
    Product <|-- Food
    Electronics <|-- Smartphone
    Electronics <|-- Laptop
    Clothing <|-- TShirt
    Clothing <|-- Jacket
    Food <|-- Milk
    Food <|-- Bread

    ProductFactory <|-- SmartphoneFactory
    ProductFactory <|-- LaptopFactory
    ProductFactory <|-- TShirtFactory
    ProductFactory <|-- JacketFactory
    ProductFactory <|-- MilkFactory
    ProductFactory <|-- BreadFactory

    SmartphoneFactory ..> Smartphone : creates
    LaptopFactory ..> Laptop : creates
    TShirtFactory ..> TShirt : creates
    JacketFactory ..> Jacket : creates
    MilkFactory ..> Milk : creates
    BreadFactory ..> Bread : creates

    Warehouse o-- "*" Product : contains
    Warehouse ..> WarehouseIterator : creates
    WarehouseIterator --> Product : iterates
```

**Модули:** `products.py`, `warehouse.py`, `product_factory.py`, `scenarios.py`, `main.py`.

---

<a id="work-2"></a>
## Работа 2 — Интерфейсы классов, взаимодействие классов, перегрузка операций

**Система:** управление заказами, способами доставки и акциями.

- `OrderManager` — создание заказов, отслеживание статусов, лимиты активных заказов,
  учёт оборота и количества клиентов.
- 3 способа доставки: `CourierDelivery`, `PickupDelivery`, `PostDelivery` — с расчётом
  стоимости, времени и проверкой доступности по весу и региону.
- 4 акции: `PercentDiscount`, `CashbackDiscount`, `FreeDeliveryDiscount`, `GiftDiscount`.
- Паттерны:
  - **Наблюдатель** — `IObserver` / `IObservable` / `OrderEvent`; `OrderManager` обновляет
    статистику при смене статуса заказа;
  - **Прокси** — `DeliveryProxy`: делегирование через `__getattr__`, проверка доступности,
    кеширование стоимости, автоматический fallback на альтернативную доставку;
  - **Стратегия** — интерфейсы `Discount` и `Delivery` с набором конкретных стратегий;
  - **Легковес** — `ProductType` с общим пулом и каталогом `ProductCategory`.
- Идиоматичные операции взаимодействия: `order + discount` (`__add__`), `order - product`
  (`__sub__`), `delivery << order` (`__lshift__`), вывод `str(order)`; для неподдерживаемых
  типов возвращается `NotImplemented`, деловые операции доступны и именованными методами.
- Явное клонирование изменяемого состояния: `Product.clone()` и `Order.clone()`
  (подписчики не копируются).
- Python-особенности: `abc.ABC` + `@abstractmethod`, snake_case, свойства `@property`
  вместо `get_*`, точка входа `main()` + `if __name__ == "__main__"`.
- Логирование всех операций с источниками `ORDER`, `DELIVERY`, `DISCOUNT`, `MANAGER`.
- 5 демонстрационных сценариев.

### UML-диаграмма классов

```mermaid
classDiagram
    class IObserver {
        <<interface>>
        +on_order_event(event)
    }
    class IObservable {
        <<interface>>
        +subscribe(observer)
        +unsubscribe(observer)
        +notify(event)
    }
    class OrderManager {
        -orders
        -customers
        -turnover
        -active_orders_count
        +create_order(customer, region, items)
        +update_status(order_id, status)
        +on_order_event(event)
        +turnover
        +active_orders_count
        +customer_count
    }
    class Order {
        -id
        -customer
        -region
        -items
        -status
        -delivery
        -discounts
        -total_price
        +__add__(discount)
        +__sub__(product)
        +__str__()
        +clone()
        +add_item(item)
        +remove_item(id)
        +set_status(status)
        +apply_discount(discount)
        +set_delivery(delivery)
        +total_weight
        +total_price
    }
    class Customer {
        -id
        -name
        -cashback_amount
        +add_cashback(amount)
    }
    class Product {
        -id
        -quantity
        -current_price
        -type
        +weight
        +total_price
        +change_quantity(delta)
    }
    class ProductType {
        -category
        -base_weight
        -base_price
        -pool$
        -catalog$
        +get_type(category)$
        +register_type(category, weight, price)$
    }
    class Delivery {
        <<abstract>>
        +name
        +get_cost(order)
        +get_estimated_time(order)
        +is_available(order)
        +__lshift__(order)
    }
    class CourierDelivery
    class PickupDelivery
    class PostDelivery
    class DeliveryProxy {
        -real_delivery
        -chosen_delivery
        -cost_cache
        -delivery_cache
        +__getattr__(attr)
        +get_cost(order)
        +get_estimated_time(order)
        +is_available(order)
        +choose_delivery(order)
    }
    class Discount {
        <<abstract>>
        +name
        +apply(order)
    }
    class PercentDiscount
    class CashbackDiscount
    class FreeDeliveryDiscount
    class GiftDiscount
    class OrderEvent {
        +order_id
        +old_status
        +new_status
        +timestamp
    }
    class Logger {
        +log(source, message)
        +records
    }
    class LoggingSource {
        <<enumeration>>
        ORDER
        DELIVERY
        DISCOUNT
        MANAGER
    }

    IObserver <|.. OrderManager
    IObservable <|.. Order
    OrderManager --> Order : observes
    Order --> Customer
    Order "1" o-- "*" Product
    Product --> ProductType : shared instance
    Order --> Delivery
    Order o-- Discount
    Delivery <|-- CourierDelivery
    Delivery <|-- PickupDelivery
    Delivery <|-- PostDelivery
    Delivery <|-- DeliveryProxy
    DeliveryProxy o-- Delivery : real + alternatives
    Discount <|-- PercentDiscount
    Discount <|-- CashbackDiscount
    Discount <|-- FreeDeliveryDiscount
    Discount <|-- GiftDiscount
    IObservable ..> OrderEvent
    IObserver ..> OrderEvent
    Logger --> LoggingSource
```

**Модули:** `manager/`, `order/`, `product/`, `delivery/`, `discount/`, `observer/`,
`customer/`, `logging/`, `scenarios.py`, `main.py`.
