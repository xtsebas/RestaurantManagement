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