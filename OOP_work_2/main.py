from decimal import Decimal, getcontext
from initialization import catalog_initialization

getcontext().prec = 28
catalog_initialization()

import msvcrt

commands = [
    "Создать файл",
    "Открыть файл",
    "Удалить файл",
    "Настройки",
    "Выход"
]

selected = 0

while True:
    print("\033[H\033[J", end="")

    print("Выберите команду:\n")

    for i, command in enumerate(commands):
        if i == selected:
            print(f"\033[92m[ {command} ]\033[0m")
        else:
            print(f"  {command}")

    key = msvcrt.getch()

    if key == b'\xe0':
        key = msvcrt.getch()

        if key == b'H':
            selected = (selected - 1) % len(commands)

        elif key == b'P':
            selected = (selected + 1) % len(commands)

    elif key == b'\r':
        break

print(f"\nВы выбрали: {commands[selected]}")