from warehouse import Warehouse
from factories import *
from products import Price

def get_ready_warehouse() -> Warehouse:
    main_warehouse = Warehouse(100)
    phone_factory = SmartphoneFactory()
    laptop_factory = LaptopFactory()
    tshirt_factory = TShirtFactory()
    jacket_factory = JacketFactory()
    milk_factory = MilkFactory()
    bread_factory = BreadFactory()
    main_warehouse.add_product(phone_factory.create_product("Apple iPhone 18 Pro 256 ГБ черный", 157999, 100, 0.21))
    main_warehouse.add_product(phone_factory.create_product("Samsung Galaxy S26 Ultra 256 ГБ черный", 109999, 158, 0.21))
    main_warehouse.add_product(phone_factory.create_product("Google Pixel 11 Pro 128 ГБ серый", 99999, 85, 0.20))
    main_warehouse.add_product(laptop_factory.create_product("Apple MacBook Pro M5 Max серебристый", 549999, 30, 2.15))
    main_warehouse.add_product(laptop_factory.create_product("ASUS ROG Strix SCAR 18 черный", 349999, 45, 3.10))
    main_warehouse.add_product(laptop_factory.create_product("Lenovo Legion Pro 7i серый", 289999, 60, 2.60))
    main_warehouse.add_product(tshirt_factory.create_product("Футболка белая", 999, 1000, 0.2))
    main_warehouse.add_product(tshirt_factory.create_product("Футболка чёрная", 999, 1000, 0.2))
    main_warehouse.add_product(tshirt_factory.create_product("Футболка красная", 999, 1000, 0.2))
    main_warehouse.add_product(jacket_factory.create_product("Мужская зимняя куртка Columbia черный", 18999, 40, 1.20))
    main_warehouse.add_product(jacket_factory.create_product("Женский пуховик Bask красный", 29999, 25, 1.45))
    main_warehouse.add_product(jacket_factory.create_product("Ветровка ветрозащитная RedFox синий", 8499, 60, 0.55))
    main_warehouse.add_product(milk_factory.create_product("Молоко Простоквашино 3.2% 930 мл", 99, 500, 0.96))
    main_warehouse.add_product(milk_factory.create_product("Молоко Пармалат ультрапастеризованное 1.8% 1 л", 129, 350, 1.03))
    main_warehouse.add_product(milk_factory.create_product("Молоко Домик в деревне 2.5% 950 мл", 95, 420, 0.98))
    main_warehouse.add_product(bread_factory.create_product("Хлеб Бородинский формовой 400 г", 45, 200, 0.40))
    main_warehouse.add_product(bread_factory.create_product("Батон Нарезной пшеничный 350 г", 38, 300, 0.35))
    main_warehouse.add_product(bread_factory.create_product("Хлеб Дарницкий традиционный 650 г", 52, 180, 0.65))
    return main_warehouse

def scenario_1():
    print("=== Сценарий 1: создание склада, добавление товаров и обход итератором ===\n")

    print("1) Создаём склад на 100 товаров")
    main_warehouse = get_ready_warehouse()


    print(f"На склад добавлено «{main_warehouse.size}» товаров")
    print("3) Вывод всех товаров через итератор:\n")
    for product in main_warehouse:
        print(product.info())

def scenario_2():
    print("=== Сценарий 2: копирование склада, изменение товара в копии и проверка независимости оригинального склада ===\n")

    main_warehouse = get_ready_warehouse()

    print("1) Копируем склад")
    new_warehouse = main_warehouse.copy()

    main_product_1 = main_warehouse.find_by_id(1)
    main_product_11 = main_warehouse.find_by_id(11)
    new_product_1 = new_warehouse.find_by_id(1)
    new_product_11 = new_warehouse.find_by_id(11)

    print("2) На новом складе поставим цену «1.000.000» и уменьшим количество на 15 для товаров с ID «1» и «11»")
    new_product_1.set_price(Price(1000000))
    new_product_1.change_quantity(-15)
    new_product_11.set_price(Price(1000000))
    new_product_11.change_quantity(-15)

    print("3) Для проверки независимости складов выведем товары с ID «1» и «11» с обоих складов:\n")

    print(f"Оригинал:\n{main_product_1.info()}")
    print(f"Копия:\n{new_product_1.info()}")
    print(f"Оригинал:\n{main_product_11.info()}")
    print(f"Копия:\n{new_product_11.info()}")

def scenario_3():
    print("=== Сценарий 3: перемещение склада через конструктор перемещения, проверка отсутствия копирования ===\n")

    print("1) Создаём склад и сохраняем его адреса")
    main_warehouse = get_ready_warehouse()
    ids_before = [id(product) for product in main_warehouse]
    list_id_before = id(main_warehouse.products)

    print("2) Перемещаем склад и тоже сохраняем адреса")
    new_warehouse = Warehouse(main_warehouse.max_size)
    new_warehouse.move_from(main_warehouse)
    ids_after = [id(product) for product in new_warehouse]
    list_id_after = id(new_warehouse.products)

    print("3) Сравниваем оба склада для проверки на перемещение:")
    print(f"\nПеремещение:\n"
          f"1. Список тот же? {{{list_id_before == list_id_after}}}\n"
          f"2. Товары те же? {{{ids_before == ids_after}}}\n"
          f"3. Источник пуст? {{{main_warehouse.products == [] and main_warehouse.size == 0}}}"
          )

    ok = (list_id_before == list_id_after and ids_before == ids_after and (len(main_warehouse.products) == 0 and main_warehouse.size == 0))
    print(f"Перемещение без копирования: {{{ok}}}")

def scenario_4():
    print("=== Сценарий 4: поиск товаров по ID, категории и цене, удаление по ID и индексу ===\n")

    main_warehouse = get_ready_warehouse()

    print("1.1) Найдём товары с ID: 1, 9, 13 и выведем их:\n")
    print(main_warehouse.find_by_id(1).info())
    print(main_warehouse.find_by_id(9).info())
    print(main_warehouse.find_by_id(13).info())
    print("1.2) Попробуем найти товар с несуществующим ID: 100000:")
    result = main_warehouse.find_by_id(100000)
    if result is None:
        print("Результат | Товара с таким ID не существует\n")

    print("2) Выведем все товары из категорий «electronics» и «food»:\n")
    print("2.1) Категория «electronics»:")
    for product in main_warehouse.find_by_category("electronics"):
        print(product.info())
    print("\n2.2) Категория «food»:")
    for product in main_warehouse.find_by_category("food"):
        print(product.info())
    print("2.3) Попробуем найти товар с несуществующей категорией:")
    temp_result = main_warehouse.find_by_category("furniture")
    for product in temp_result:
        print(product.info())
    print(f"Результат | Длина списка: {len(temp_result)}\n")

    print("3) Найдём товары по цене «95» и «999»:\n")
    print("3.1) Цена «95»:")
    for product in main_warehouse.find_by_price(Price(95)):
        print(product.info())
    print("3.2) Цена «999»:")
    for product in main_warehouse.find_by_price(Price(999)):
        print(product.info())
    print("3.3) Попробуем найти товар с несуществующей ценой:")
    temp_result = main_warehouse.find_by_price(Price(9999999))
    for product in temp_result:
        print(product.info())
    print(f"Результат | Длина списка: {len(temp_result)}\n")

    print("4) Удалим товары с ID «4» и «6»:\n")
    main_warehouse.remove_by_id(4)
    main_warehouse.remove_by_id(6)
    print("Список товаров после удаления:\n")
    for product in main_warehouse:
        print(product.info())
    print("4.1) Попробуем удалить с несуществующим ID:")
    try:
        main_warehouse.remove_by_id(99999)
    except ValueError:
        print("Результат | Товар с таким ID не найден!\n")

    print("5) Удалим товары с индексами «0» и «1»:\n")
    main_warehouse.remove_by_index(0)
    print("Список товаров после удаления товара с индексом «0»:\n")
    for product in main_warehouse:
        print(product.info())
    main_warehouse.remove_by_index(1)
    print("Список товаров после удаления товара с индексом «1» (после первого изменения):\n")
    for product in main_warehouse:
        print(product.info())
    print("5.1) Попробуем удалить с несуществующим индексом:")
    try:
        main_warehouse.remove_by_index(59744)
    except IndexError:
        print("Результат | Выход за пределы массива!\n")

def scenario_5():
    print("=== Сценарий 5: перемещение товара между складами через TransferTo, изменение остатков и цены ===\n")

    print("1) Создадим два склада: один с товарами, другой без товаров")
    main_warehouse = get_ready_warehouse()
    new_warehouse = Warehouse(30)
    print("Cклады до переноса:")
    print(f"Товаров на первом складе: {len(main_warehouse.products)}")
    print(f"Товаров на втором складе: {len(new_warehouse.products)}")

    print("\n2) Перенесём товары с ID: 1, 5, 9 на новый склад без товаров")
    main_warehouse.find_by_id(1).transfer_to(new_warehouse)
    main_warehouse.find_by_id(5).transfer_to(new_warehouse)
    main_warehouse.find_by_id(9).transfer_to(new_warehouse)

    print("Cклады после переноса:")
    print(f"Товаров на первом складе: {len(main_warehouse.products)}")
    print(f"Товаров на втором складе: {len(new_warehouse.products)}")
    print("\nНовый склад после переноса:\n")
    for product in new_warehouse:
        print(product.info())

    print("3) Изменим остаток для каждого товара на новом складе (уберём по 5 товаров)")
    for product in new_warehouse:
        product.change_quantity(-5)
    print("\nСписок товаров после изменения:\n")
    for product in new_warehouse:
        print(product.info())

    print("4) Установим всем товарам на новом складе цену «1»")
    for product in new_warehouse:
        product.set_price(Price(1))
    print("\nСписок товаров после изменения:\n")
    for product in new_warehouse:
        print(product.info())