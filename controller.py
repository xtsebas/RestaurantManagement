import psycopg2

def validar_mesa(no_mesa, area_id, connection):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM mesa WHERE area_id = "+area_id+" AND no_mesa = "+no_mesa+';'
        cursor.execute(query)

        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        print(rows)
        print(len(rows))
        return rows
    except (Exception, psycopg2.Error) as error:
        print("Error al obtener mesas:", error)
        return []

def mesa_disponible(no_mesa, connection):
    try:
        cursor = connection.cursor()
        query = "SELECT estado FROM mesa WHERE no_mesa = %s;"
        cursor.execute(query, (no_mesa,))  # Pass no_mesa as a parameter

        row = cursor.fetchone()  # Assuming each 'no_mesa' has exactly one row
        cursor.close()
        estado = row[0]
        print("estado: "+str(estado))

        if estado == False: #Si la mesa no esta ocupada
            print("Mesa libre")
        else:
            print("La mesa se encuetra ocupada o olvido cerrar la cuenta")
        
    except (Exception, psycopg2.Error) as error:
        print("Error con la mesa", error)
        return False  # Return False on error or handle as needed
    
def validar_calificacion(campo: str):
    while True:
        print("\nEn un rango de 1 al 5 califique la "+campo+" del servicio")
        try:
            calificacion = int(input("Ingrese la nota => "))
            if calificacion >= 1 and calificacion <= 5:
                return calificacion
            else:
                print("Por favor ingrese un numero valido")
        except:
            print("Por favor ingrese un caracter valido")

def validar_opcion_queja(valor:str):
    valores = [1,2]
    while True:
        print("Es una queja relacionada con algun ",valor)
        print("==========\n1. Si\n2. No\n==========\n")
        try:
            opcion = int(input("Ingrese su respuesta => "))
            if opcion in valores:
                if opcion == 1:
                    return True
                else:
                    return False
            else:
                print("Ingrese una opcion valida")
        except:
            print("Ingresar un caracter valido")

        return False  # Return False on error or handle as needed
