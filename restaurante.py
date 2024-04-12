from db_test1 import *
from tabulate import tabulate
import os
from controller import *

def ordernar():
    return None

def abrirCuenta():
    return None

def cerrarCuenta():
    return None

def opcionesMesa():
    print("================================")
    print("Acciones con la mesa")
    print("1. Abrir cuenta")
    print("2. Cerrar cuenta/generar factura")
    print("3. Ordenar")
    print("4. Regresar")
    print("================================")


    while True:
        opcionMesa = str(input("Ingresa accion con la mesa: "))

        if opcionMesa == "1":
            abrirCuenta()
        elif opcionMesa == "2":
            cerrarCuenta()
        elif opcionMesa == "3":
            ordernar()
        elif opcionMesa == "4":
            print("Regeresando")
            break

    return None 

def accionMesa(area,connection):
    print("\nUsted Puede realizar:")
    print("1. Seleccionar mesa 2. Regresar")
    accion = str(input('Ingrese la accion: '))
    
    if accion == "1":
        print("ID AREA: "+area)
        no_mesa  = str(input(("Ingrese el numero de mesa: ")))
        nombre_area = obtener_area(connection=connection,area_id=area)
        
        if len(validar_mesa(no_mesa=no_mesa, area_id=area,connection=connection)) == 1:
            print("Valid")
            opcionesMesa()
        else:
            print("Mesa no esta en esta area")

    elif accion == "2":
        pass


def opcionesMesas():
    print("Usted Puede realizar:")
    print("1. Elegir Area       2. Juntar Mesas     3. Escribir una queja")
    return str(input("\nIngrese el su opcion deseada: "))


#mostrar mesas
def mesas(database):
    opcion = opcionesMesas()
    
    if opcion=='1':
        print("\nElige el area")
        pantalla_area = obtener_areas(database)
        headers = ["ID", "Nombre", "Tipo"]
        print(tabulate(pantalla_area, headers=headers))
        area = str(input("\nIngrese el id del area: "))
        
        headers = ["Numero de mesa", "Capacidad", "Estado", "Esta Unida"]
        pantalla_mesas = obtener_mesas(database, area)
        if pantalla_mesas == []:
            pass
        else:
            print("\n" + tabulate(pantalla_mesas, headers=headers))
            accionMesa(area=area, connection=database)

        
    elif opcion=='2':
        pass
    elif opcion=='3':
        pass
    


database = conectar_bd()

while True:

    print("\n=====================")
    print("Manejo de restaurante")
    print("=====================")
    print("1. Pantalla de Mesas")
    print("2. Pantalla de cocina")
    print("3. Pantalla de bar")
    print("4. Reportes")

    accion = str(input("Ingrese la pantalla: "))
    #Limpia la consola
    os.system('cls' if os.name == 'nt' else 'clear')

    if accion == "1":
        mesas(database=database)

    elif accion == "2":
        print("\nPantalla de cocina")
        pantalla_cocina = obtener_cocina(database)
        headers = ["Cuenta", "Cantidad", "Plato", "Fecha"]
        print(tabulate(pantalla_cocina, headers=headers))
        
    elif accion == "3":
        print("\nPantalla de bar")
        pantalla_bar = obtener_bar(database)
        headers = ["Cuenta", "Cantidad", "Bebida", "Fecha"]
        print(tabulate(pantalla_bar, headers=headers))

    elif accion == "4":
        print("\nReportes")
        print("\n1. Platos mas pedidos por clientes\n2. Horario donde se ingresan mas pedidos\n3. Promedio de tiempo que tardan los clientes en comer\n4. Quejas agrupadas por persona\n5. Quejas agrupadas por item\n6. Eficiencia de los meseros por sus encuestas")
        reporte = str(input("Ingrese la pantalla: "))
        
        if reporte=="1":
            print("1")
            
        elif reporte=="2":
            print("1")
            
        elif reporte=="3":
            print("1")
            
        elif reporte=="4":
            print("1")
            
        elif reporte=="5":
            print("1")
            
        elif reporte=="6":
            print("1")
    
        
        """
        menu = obtener_menu(database)
        headers = ["ID", "Nombre", "Descripción", "Precio", "Tipo"]

        print(tabulate(menu, headers=headers))
        """

