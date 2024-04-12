import psycopg2

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
        query = "SELECT * FROM items"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except (Exception, psycopg2.Error) as error:
        print("Error al obtener el menú:", error)
        return []
    
def obtener_cocina(connection):
    try:
        cursor = connection.cursor()
        query = ""
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
            select no_mesa , capacidad, estado, unida from mesa 
            where area_id = %s
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
            SELECT pedidos.id_cuenta, pedidos.cantidad, items.nombre, pedidos.fecha 
            FROM pedidos
            INNER JOIN items ON pedidos.item_id = items.item_id
            WHERE items.tipo = 'Comida'
            ORDER BY pedidos.fecha DESC;
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
        SELECT pedidos.id_cuenta, pedidos.cantidad, items.nombre, pedidos.fecha 
        FROM pedidos
        INNER JOIN items ON pedidos.item_id = items.item_id
        WHERE items.tipo = 'Bebida'
        ORDER BY pedidos.fecha DESC;
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

def db_signIn(
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

