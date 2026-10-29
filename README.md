```mermaid
classDiagram
    class Price {
        -_value: int
        +value: int
    }
    
    class Quantity {
        -_value: int
        +value: int
        +change(delta: int)
    }
    
    class Weight {
        -_value: float
        +value: float
    }
    
    class Product {
        <<abstract>>
        -_next_id: int
        -_id: int
        -_name: str
        -_category: str
        -_price: Price
        -_quantity: Quantity
        -_weight: Weight
        -_warehouse: Warehouse
        +clone()* Product
        +change_quantity(delta: int)
        +set_price(new_price: Price)
        +transfer_to(other: Warehouse)
        +info(): str
    }
    
    Product *-- Price
    Product *-- Quantity
    Product *-- Weight
    Product --> Warehouse : _warehouse

    class Electronics {
        <<abstract>>
    }
    class Clothing {
        <<abstract>>
    }
    class Food {
        <<abstract>>
    }

    Product <|-- Electronics
    Product <|-- Clothing
    Product <|-- Food

    class Smartphone
    class Laptop
    class TShirt
    class Jacket
    class Milk
    class Bread

    Electronics <|-- Smartphone
    Electronics <|-- Laptop
    Clothing <|-- TShirt
    Clothing <|-- Jacket
    Food <|-- Milk
    Food <|-- Bread

    class ProductFactory {
        <<abstract>>
        +create_product(...)* Product
    }

    class SmartphoneFactory
    class LaptopFactory
    class TShirtFactory
    class JacketFactory
    class MilkFactory
    class BreadFactory

    ProductFactory <|-- SmartphoneFactory
    ProductFactory <|-- LaptopFactory
    ProductFactory <|-- TShirtFactory
    ProductFactory <|-- JacketFactory
    ProductFactory <|-- MilkFactory
    ProductFactory <|-- BreadFactory

    class Warehouse {
        -_products: list
        -_max_size: int
        -_current_size: int
        +size: int
        +max_size: int
        +products: list
        +copy() Warehouse
        +copy_from(other: Warehouse)
        +move_from(other: Warehouse)
        +add_product(product: Product)
        +remove_by_id(id: int): bool
        +remove_by_index(index: int)
        +find_by_id(id: int): Product
        +find_by_category(category: str): list
        +find_by_price(price: Price): list
    }

    Warehouse o-- Product : _products
