import psycopg2 # type: ignore
from datetime import datetime
import pdb #Debuggear
from tabulate import tabulate # type: ignore


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
                values(%s, %s, %s, CURRENT_TIMESTAMP)
            """
            cursor.execute(cuenta, (no_mesa, id_empleado,'inactiva'))
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

def get_empleados(connection):
    try:
        cursor = connection.cursor()
        query = "SELECT empleado_id, nombre_empleado FROM empleado;"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        
        headers = ["ID EMPLEADO", "NOMBRE EMPLEADO"]
        print(tabulate(rows, headers=headers))
        return rows
    except (Exception, psycopg2.Error) as error:
        print("Error al obtener el menú:", error)
        return []
    

def get_cuentas(connection):
    try:
        cursor = connection.cursor()
        query = "select id_cuenta from cuenta LIMIT 10;"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        
        headers = ["ID CUENTA"]
        print(tabulate(rows, headers=headers))
        return rows
    except (Exception, psycopg2.Error) as error:
        print("Error al obtener el menú:", error)
        return []

def get_items(connection):
    try:
        cursor = connection.cursor()
        query = "SELECT item_id, nombre from items;"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        
        headers = ["ID PLATO/BEBIDA", "NOMBRE"]
        print(tabulate(rows, headers=headers))
        return rows
    except (Exception, psycopg2.Error) as error:
        print("Error al obtener el menú:", error)
        return []
    
def submit_encuesta_final(connection, empleado_id, cuenta_id, amabilidad, exactitud):
    """Insert survey data into the encuesta_final table."""
    # SQL command to insert data
    query = """
    INSERT INTO encuesta_final (empleado_id, cuenta_id, amabilidad, exactitud)
    VALUES (%s, %s, %s, %s);
    """
    try:
        # Create a cursor object using the connection
        cursor = connection.cursor()
        # Execute the query with provided data
        cursor.execute(query, (empleado_id, cuenta_id, amabilidad, exactitud))
        # Commit the changes to the database
        connection.commit()
        print("Encuesta submitted successfully.")
    except psycopg2.Error as e:
        # If an error occurs, rollback any changes made during the transaction
        connection.rollback()
        print(f"An error occurred while submitting the encuesta: {e}")
    finally:
        # Always close the cursor to release database resources
        cursor.close()    

def submit_queja(connection, empleado_id, item_id, nit_cliente, clasificacion, motivo):
    """Insert complaint data into the queja table with potential NULL values for employee or item IDs."""
    query = """
    INSERT INTO queja (empleado_id, item_id, nit_cliente, fecha, calificacion, motivo)
    VALUES (%s, %s, %s, NOW(), %s, %s);
    """
    try:
        cursor = connection.cursor()
        # Handling potential NULL values for empleado_id and item_id
        empleado_id = empleado_id or None  # This will pass None if empleado_id is an empty string
        item_id = item_id or None  # This will pass None if item_id is an empty string
        cursor.execute(query, (empleado_id, item_id, nit_cliente, clasificacion, motivo))
        connection.commit()
        print("Queja submitted successfully with the current date and time.")
    except Exception as e:
        connection.rollback()
        print(f"An error occurred while submitting the queja: {e}")
    finally:
        cursor.close()
        
#Ingresar pedido
def ingresar_pedido(pedido, cantidad, no_mesa, connection):
    cursor = connection.cursor()
    query="""
        select id_cuenta from cuenta
        where no_mesa = %s and estado = 'activa'
    """
    cursor.execute(query, (no_mesa,))
    resultado = cursor.fetchone()
    if resultado:
        id_cuenta = int(resultado[0])  
        print(id_cuenta)
        query2="""
            insert into pedidos(id_cuenta, item_id, cantidad, fecha)
            values (%s, %s, %s, now())
        """
        cursor.execute(query2, (id_cuenta, pedido, cantidad))
        connection.commit()
        print("Agregado a la cuenta exitosamente")
    else:
        print("No se encontró una cuenta activa para la mesa especificada.")
        
#cerrar una cuenta
def cerrar_cuenta(no_mesa, connection):
    cursor = connection.cursor()
    query = """
        SELECT no_mesa, empleado_asociado, estado FROM cuenta
        WHERE no_mesa = %s and estado = 'activa'
    """
    try:
        cursor.execute(query, (no_mesa,))
        result = cursor.fetchone()
        
        if not result:
            return "La cuenta ya está cerrada"

        estado = result[2]
        if estado == 'activa':
            update_query = """
                UPDATE cuenta
                SET estado = 'cerrada',
                    hora_salida = now()
                WHERE no_mesa = %s
            """
            cursor.execute(update_query, (no_mesa,))
            update_query2 = """
                UPDATE mesa
                SET estado = FALSE,
                WHERE no_mesa = %s
            """
            cursor.execute(update_query2, (no_mesa,))
            connection.commit()
            return "La cuenta ha sido cerrada exitosamente"
        else:
            return "La cuenta no ha sido abierta"

    except Exception as e:
        return "Error al procesar la solicitud: {}".format(str(e))



#Reporte de platos pedidos en cierto rango de fecha
def platos_pedidos(inicial, final, connection):
    cursor = connection.cursor()
    query = """
        SELECT i.nombre AS plato, COUNT(p.item_id) AS cantidad_pedidos
        FROM pedidos p
        JOIN items i ON p.item_id = i.item_id
        WHERE p.fecha BETWEEN %s AND %s
        GROUP BY i.nombre, p.item_id
        ORDER BY COUNT(p.item_id) DESC
    """
    try:
        cursor.execute(query, (inicial, final))
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except (Exception, psycopg2.Error) as error:
        print("Error al obtener el reporte:", error)
        return []

#Reporte de hora donde se realizan mas pedidos en cierto rango de fecha
def horario_pedidos(inicial, final, connection):
    cursor = connection.cursor()
    query = """
        SELECT EXTRACT(HOUR FROM fecha) AS hora_del_dia, COUNT(*) AS cantidad_pedidos
        FROM pedidos
        WHERE fecha BETWEEN %s AND %s
        GROUP BY EXTRACT(HOUR FROM fecha)
        ORDER BY cantidad_pedidos DESC;
    """
    try:
        cursor.execute(query, (inicial + ' 00:00:00', final + ' 23:59:59'))
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except (Exception, psycopg2.Error) as error:
        print("Error al obtener el reporte:", error)
        return []

#Reporte de promedio de tiempo que tardan los clientes en comer agrupados en personas en cierto rango de fecha
def personas_tiempo(inicial, final, connection):
    cursor = connection.cursor()
    query = """
        SELECT 
            personas,
            EXTRACT(HOUR FROM AVG(tiempo_comida)) AS horas_promedio,
            EXTRACT(MINUTE FROM AVG(tiempo_comida)) AS minutos_promedio
        FROM (
            SELECT a.capacidad as personas, (b.hora_salida - b.hora_entrada) as tiempo_comida from mesa a 
            join cuenta b on a.no_mesa = b.no_mesa
            where b.estado = 'cerrada' and b.hora_salida notnull and b.hora_salida between %s AND %s
        ) AS tiempos_por_cuenta
        GROUP BY personas
        ORDER BY personas;
    """
    try:
        cursor.execute(query, (inicial, final))
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except (Exception, psycopg2.Error) as error:
        print("Error al obtener el reporte:", error)
        return []