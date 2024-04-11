from db_test1 import conectar_bd, obtener_menu,obtener_cocina,obtener_bar
from tabulate import tabulate

database = conectar_bd()

while True:

    print("=====================")
    print("Manejo de restaurante")
    print("=====================")
    print("1. Pantalla de cocina")
    print("2. Pantalla de bar")
    print("3. Ver items")

    accion = str(input("Ingrese la pantalla: "))

    if accion == "1":
        print("Pantalla de cocina")
        pantalla_cocina = obtener_cocina(database)
        headers = ["Cuenta", "Cantidad", "Plato", "Fecha"]
        print(tabulate(pantalla_cocina, headers=headers))

    elif accion == "2":
        print("Pantalla de bar")
        pantalla_bar = obtener_bar(database)
        headers = ["Cuenta", "Cantidad", "Bebida", "Fecha"]
        print(tabulate(pantalla_bar, headers=headers))

    elif accion == "3":
        print("Extrayendo items")
        menu = obtener_menu(database)
        headers = ["ID", "Nombre", "Descripción", "Precio", "Tipo"]

        print(tabulate(menu, headers=headers))

