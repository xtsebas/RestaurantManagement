import psycopg2
from datetime import datetime
import pdb #Debuggear

def conectar_bd():
    try:
        # Conectarse a la base de datos
        connection = psycopg2.connect(
            user="u9h73gvdn3nqqq",
            password="p3a93c7dd4442cdfc25db1687dadde248f90752ba646cd88e60fa4a95c3c119fd",
            host="c7gljno857ucsl.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com",
            port="5432",
            database="dbqa0v50s9e961"
        )
        print("Conexión a PostgreSQL exitosa")
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error al conectar a PostgreSQL:", error)
        return None

def obtener_menu(connection):
    try:
        cursor = connection.cursor()
        query = "SELECT item_id, nombre, descripcion, precio FROM items"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except (Exception, psycopg2.Error) as error:
        print("Error al obtener el menú:", error)
        return []
    
def obtener_areas(connection):
    try:
        cursor = connection.cursor()
        query = """
            select * from area
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except (Exception, psycopg2.Error) as error:
        print("Error al obtener mesas:", error)
        return []

def obtener_mesas(connection, area_id):
    try:
        cursor = connection.cursor()
        query = """
        SELECT no_mesa, capacidad, estado, unida FROM mesa 
        WHERE area_id = %s
        ORDER BY no_mesa ASC
        """
        cursor.execute(query, (area_id))
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except (Exception, psycopg2.Error) as error:
        print("Error al obtener mesa o mesa invalida:", error)
        return []

def obtener_cocina(connection):
    try:
        cursor = connection.cursor()
        # Define the SQL query
        query = """
            SELECT pedidos.id_cuenta, 
            pedidos.cantidad, 
            items.nombre, 
            DATE(pedidos.fecha) as fecha 
            FROM pedidos
            INNER JOIN items ON pedidos.item_id = items.item_id
            WHERE items.tipo = 'Comida'
            ORDER BY fecha DESC;

        """
        # Execute the SQL query
        cursor.execute(query)
        # Fetch all rows matching the query
        rows = cursor.fetchall()
        # Close the cursor
        cursor.close()
        # Return the fetched rows
        return rows
    except (Exception, psycopg2.Error) as error:
        print("Error al obtener el menú:", error)
        # Return an empty list in case of error
        return []
    
def obtener_bar(connection):
    try:
        cursor = connection.cursor()
        # Define the SQL query
        query = """
            SELECT pedidos.id_cuenta, 
            pedidos.cantidad, 
            items.nombre, 
            DATE(pedidos.fecha) AS fecha 
            FROM pedidos
            INNER JOIN items ON pedidos.item_id = items.item_id
            WHERE items.tipo = 'Bebida'
            ORDER BY fecha DESC;

        """
        cursor.execute(query)
        rows = cursor.fetchall()
        # Close the cursor
        cursor.close()
        # Return the fetched rows
        return rows
    except (Exception, psycopg2.Error) as error:
        print("Error al obtener el menú:", error)
        # Return an empty list in case of error
        return []

def obtener_area(connection, area_id):
    try:
        cursor = connection.cursor()
        query = "SELECT nombre_area FROM area WHERE area_id = "+area_id
        cursor.execute(query)

        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except (Exception, psycopg2.Error) as error:
        print("Error al obtener mesas:", error)
        return []

#registro de usuarios
def db_register(
            connection,
            nombre_empleado,
            rol,
            area_asignada,
            hash_password,
        ):
        cursor = connection.cursor()
        query = """
                INSERT INTO empleado (nombre_empleado, contrasena_hash, rol, area_asignada) 
                VALUES (%s, %s, %s, %s);
                """
        try:
            # Execute the query and commit changes
            cursor.execute(query, (nombre_empleado, hash_password, rol, area_asignada))
            connection.commit()
            print("Empleado registrado exitosamente.")
        except (Exception, psycopg2.Error) as error:
            print("Error al registrar el empleado:", error)
        finally:
            # Close the database connection
            if connection:
                cursor.close()
                connection.close()

        return None

#sign in con verificacion de usuario
def db_signin(connection, usuario, contrasena):
    cursor = connection.cursor()
    query = """
        SELECT * FROM empleado
        WHERE nombre_empleado = %s AND contrasena_hash = %s
    """
    try:
        cursor.execute(query, (usuario, contrasena))
        rows = cursor.fetchall()
        return sum(rows, ())
    except Exception as e:
        print("Empleado no encontrado", e)
        return []

#estado de la mesa (ocupado o no)
def validacion_mesa(no_mesa, area_id, connection, option, id_empleado):
    #pdb.set_trace() 
    cursor = connection.cursor()
    query = """
        SELECT no_mesa, area_id, estado, unida FROM mesa
        WHERE no_mesa = %s AND area_id = %s
    """
    cursor.execute(query, (no_mesa, area_id))
    result = cursor.fetchone()
    
    if not result:
        return None
    
    estado = result[2]
    
    if option == 1:
        if estado:
            return None
        else:
            update_query = """
                UPDATE mesa
                SET estado = TRUE
                WHERE no_mesa = %s AND area_id = %s
            """
            cursor.execute(update_query, (no_mesa, area_id))
            connection.commit()
            
            cuenta = """
                insert into cuenta (no_mesa, empleado_asociado, estado, hora_entrada)
                values(%s, %s, %s, $s)
            """
            cursor.execute(cuenta, (no_mesa, id_empleado,'inactiva', datetime.now()))
            connection.commit()
            
            return [no_mesa, area_id, estado, result[3]]
    elif option == 2:
        if estado:
            return [no_mesa, area_id, estado, result[3]]
        else:
            return None

#saber si la cuenta esta inactiva, activa o cerrada        
def mesa_activa(no_mesa, connection):
    cursor = connection.cursor()
    query = """
        SELECT no_mesa, empleado_asociado, estado FROM cuenta
        WHERE no_mesa = %s
    """
    try:
        cursor.execute(query, (no_mesa,))
        result = cursor.fetchone()
        
        if not result:
            return "La cuenta ya está cerrada"
        
        estado = result[2]
        if estado == 'activa':
            return "La cuenta ya está abierta"
        else:
            update_query = """
                UPDATE cuenta
                SET estado = 'activa'
                WHERE no_mesa = %s
            """
            cursor.execute(update_query, (no_mesa,))
            connection.commit()
            return "La cuenta ha sido abierta exitosamente"
    except Exception as e:
        return "Error al procesar la solicitud: {}".format(str(e))
