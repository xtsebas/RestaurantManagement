SELECT * FROM mesa;
SELECT * FROM cuenta;
SELECT * FROM empleado
SELECT * FROM pedidos;
SELECT * FROM items;


/*2 TOMA DE PEDIDO */
--Al crear cuenta
INSERT INTO cuenta (no_mesa, empleado_asociado, estado, hora_entrada, hora_salida)
VALUES (
	14, --no_mes 
	2, --empleado_asociado
	'Activa', --estado de la mesa
	CURRENT_TIMESTAMP -- tiempo de entrada, 
	NULL -- sin hora de salida
);

--tomando pedidos -- tipo comida
INSERT INTO pedidos VALUES(
	35, --id_cuenta
	20, --item_id
	1, --cantidad
	CURRENT_TIMESTAMP -- tiempo de la orden
);

--tomando bebida -- tipo comida
INSERT INTO pedidos VALUES(
	35, --id_cuenta
	10, --item_id
	1, --cantidad
	CURRENT_TIMESTAMP -- tiempo de la orden
);


/*3 PANTALLA DE COCINA */
SELECT pedidos.id_cuenta, pedidos.cantidad, items.nombre, pedidos.fecha 
FROM pedidos
INNER JOIN items ON pedidos.item_id = items.item_id
WHERE items.tipo = 'Comida'
ORDER BY pedidos.fecha DESC;


/*4 PANTALLA DE BAR */
SELECT pedidos.id_cuenta, pedidos.cantidad, items.nombre, pedidos.fecha 
FROM pedidos
INNER JOIN items ON pedidos.item_id = items.item_id
WHERE items.tipo = 'Bebida'
ORDER BY pedidos.fecha DESC;

--Al cerrar la cuenta
UPDATE cuenta 
	SET hora_salida = CURRENT_TIMESTAMP,
		estado = 'Inactiva'
WHERE id_cuenta = 35;

/*5 IMPRESION DEL PEDIDO 
Para este caso, se ira mostrando dentro del modal antes de poner la orden
*/

/*6 CIERRE DE LA CUENTA*/
--El query muestra platos, bebidas y su total
SELECT 
    items.nombre,
    SUM(pedidos.cantidad) AS cantidad,
    SUM(pedidos.cantidad) * items.precio AS total
FROM pedidos
INNER JOIN items ON pedidos.item_id = items.item_id
GROUP BY items.nombre, items.precio;

--Mostranto todo el total de la factura
SELECT 
    SUM(t.total) AS total_general
FROM (
    SELECT 
        SUM(pedidos.cantidad) * items.precio AS total
    FROM pedidos
    INNER JOIN items ON pedidos.item_id = items.item_id
    GROUP BY items.nombre, items.precio
) AS t;

-- el total con la propina incluida
SELECT 
    SUM(t.total) * 1.10 AS total_general_con_iva
FROM (
    SELECT 
        items.nombre, 
        SUM(pedidos.cantidad) AS cantidad, 
        SUM(pedidos.cantidad) * items.precio AS total
    FROM pedidos
    INNER JOIN items ON pedidos.item_id = items.item_id
    GROUP BY items.nombre, items.precio
) AS t;

--Reportes
--Reporte de los platos más pedidos por los clientes en un rango de fechas solicitadas al usuario

DROP PROCEDURE reporte_platos_mas_pedidos;

CREATE OR REPLACE PROCEDURE reporte_platos_mas_pedidos(
    p_fecha_inicio TIMESTAMP,
    p_fecha_fin TIMESTAMP
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Verificar si la tabla temporal ya existe
    IF NOT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'resultados') THEN
        -- Crear una tabla temporal para almacenar los resultados
        CREATE TEMP TABLE resultados (
            nombre_item VARCHAR,
            cantidad_pedidos INT
        );
    ELSE
        -- Eliminar los datos existentes de la tabla temporal
        TRUNCATE resultados;
    END IF;
    -- Insertar los platos más pedidos dentro del intervalo de fechas en la tabla temporal
    INSERT INTO resultados
    SELECT items.nombre, COUNT(pedidos.item_id) AS cantidad_pedidos
    FROM pedidos
    INNER JOIN items ON items.item_id = pedidos.item_id
    WHERE pedidos.fecha BETWEEN p_fecha_inicio AND p_fecha_fin
    GROUP BY items.nombre
    ORDER BY cantidad_pedidos DESC;

    -- Retornar
    RETURN;
END;
$$;



CALL reporte_platos_mas_pedidos('2023-01-01', '2024-04-30'); --llamado al procedimiento
SELECT * FROM resultados; --muestra de resultados con platos--
