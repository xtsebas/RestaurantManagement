from db_test1 import *
from tabulate import tabulate
import os
from controller import *
import bcrypt
import time
import pdb #Debuggear

"""
Funciones relacionadas con el flujo del restaurante
"""
def ordernar():
    return None

def abrirCuenta(no_mesa,connection):
    if mesa_disponible(no_mesa,connection):
        print("Cuenta abierta exitosamente")
    return None

def cerrarCuenta():
    return None

def opcionesMesa(no_mesa,connection):
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
            abrirCuenta(no_mesa, connection)
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
    print("1. Sentar clientes en una mesa    2. Atender una mesa      3. Regresar")
    accion = str(input('Ingrese la accion: '))
    
    if accion == "1":
        print("ID AREA: "+area)
        no_mesa  = str(input(("Ingrese el numero de mesa: ")))
        nombre_area = obtener_area(connection=connection,area_id=area)
        validar=validacion_mesa(no_mesa=no_mesa, area_id=area,connection=connection)
        
        #pdb.set_trace() 
        if validar is not None and len(validar) > 0:
            print("Valid")
            opcionesMesa(no_mesa,connection)
        else:
            print("Mesa no disponible")

    elif accion == "2":
        pass
    
    elif accion == "3":
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
            print("Mesa Ocupada")
        else:
            print("\n" + tabulate(pantalla_mesas, headers=headers))
            accionMesa(area=area, connection=database)

        
    elif opcion=='2':
        pass
    elif opcion=='3':
        pass
    
"""
Funciones relacionadas con el inicio de sesion
"""
def registrarse(connection):
    print("===============\nRegistro\n==============")
    nombre_empleado = str(input("Ingrese el nombre del empleado: "))
    rol = str(input("Ingrese el rol del empleado: "))
    area_asignada = str(input("Ingrese el area asignada del empleado: "))
    cotrasena = str(input("Ingrese la contrasena: "))
    hash_password = bcrypt.hashpw(cotrasena.encode('utf-8'), bcrypt.gensalt())
    print(f"Nombre: {nombre_empleado}, Rol: {rol}, Area: {area_asignada}, Contrasena: {cotrasena}, hash: {hash_password}")
    db_register(
        connection=connection,
        nombre_empleado=nombre_empleado,
        rol=rol,
        area_asignada=area_asignada,
        hash_password=hash_password
    )
    return None

"""
Funcion general del manejor del restaurante
"""
def restaurante(database):

    while True:
        
        print("\n=====================")
        print("Manejo de restaurante")
        print("=====================")
        print("1. Pantalla de Mesas")
        print("2. Pantalla de cocina")
        print("3. Pantalla de bar")
        print("4. Reportes")
        print("10. Cerrar sesion")

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

        elif accion == "10":
            break


#Flujo de sign in/ log in

database = conectar_bd()

while True:
    print("============ Restaurant managment ===========")
    print("1. Iniciar sesicion\n2. Registrarse\n3. Salir")
    accion = str(input("Ingrese su opcion ---> "))

    if accion == "1":
        usuario = str(input("Ingrese su usuario ---> "))
        contrasena = str(input("Ingrese su contraseña ---> "))
        user = db_signin(connection=database, usuario=usuario, contrasena=contrasena )
        if len(user) > 0:
            current_user = user
            user = []
            os.system('cls' if os.name == 'nt' else 'clear')
            print("INGRESO EXITOSO")
            time.sleep(3)
            time_left = 3
            while time_left > 0:
                print("Redirigiendo, quedan {} para ingresar".format(time_left))
                time.sleep(1)
                time_left -= 1
            os.system('cls' if os.name == 'nt' else 'clear')
            restaurante(database)
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("USUARIO O CONTRASEÑA INCORRECTOS, INTENTELO DE NUEVO")
    elif accion == "2":
        registrarse(connection=database)
        pass
    elif accion == "3":
        break



