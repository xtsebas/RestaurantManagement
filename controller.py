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
    
    