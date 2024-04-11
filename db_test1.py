import psycopg2

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


