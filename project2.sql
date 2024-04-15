create table items (
	item_id serial primary key,
	nombre varchar(150),
	descripcion varchar(255),
	precio numeric(10, 2),
	tipo varchar(50)
)

create table area (
	area_id serial primary key,
	nombre_area varchar(150),
	tipo_area varchar(255)
)

create table mesa (
	no_mesa serial primary key,
	area_id int,
	capacidad int, 
	estado boolean, 
	unida boolean,
	foreign key (area_id) references area(area_id)
)

create table empleado (
	empleado_id serial primary key,
	nombre_empleado varchar(150),
	contrasena_hash char(60),
	rol varchar(50),
	area_asignada varchar(20)
)

create table cuenta (
	id_cuenta serial primary key,
	no_mesa int,
	empleado_asociado int,
	estado varchar(50),
	foreign key (no_mesa) references mesa(no_mesa),
	foreign key (empleado_asociado) references empleado(empleado_id)
)

create table pedidos (
	id_cuenta int,
	item_id int,
	cantidad int,
	fecha timestamp default current_timestamp,
	foreign key (id_cuenta) references cuenta(id_cuenta),
    FOREIGN KEY (item_id) REFERENCES items(item_id)
)

create table factura (
	factura_id serial primary key,
	cuenta_id int,
	nit varchar(9),
	nombre_cliente varchar(150),
	direccion_cliente varchar(150),
	total numeric(10, 2),
	propina numeric(10, 2),
	cobro numeric(10, 2),
	fecha timestamp default current_timestamp,
	foreign key (cuenta_id) references cuenta(id_cuenta)
)

create table cliente (
	nit varchar(9) primary key,
	nombre_cliente varchar(150),
	direccion_cliente varchar(150)
)

CREATE OR REPLACE FUNCTION agregar_cliente_si_no_existe()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar si el nit existe en la tabla cliente
    IF NOT EXISTS (SELECT 1 FROM cliente WHERE nit = NEW.nit) THEN
        -- Insertar el nuevo cliente en la tabla cliente
        INSERT INTO cliente (nit, nombre_cliente, direccion_cliente)
        VALUES (NEW.nit, NEW.nombre_cliente, NEW.direccion_cliente);
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER verificar_nit_cliente
AFTER INSERT ON factura
FOR EACH ROW
EXECUTE FUNCTION agregar_cliente_si_no_existe();

create table transaccion (
	factura_id int,
	metodo varchar(100),
	monto numeric(10, 2),
	foreign key (factura_id) references factura(factura_id)
)

create table encuesta_final (
	encuesta_id serial primary key,
	empleado_id int,
	cuenta_id int,
	amabilidad int,
	exactitud int,
	foreign key (empleado_id) references empleado(empleado_id),
	foreign key (cuenta_id) references cuenta(id_cuenta)
)

create table queja (
	queja_id serial primary key,
	empleado_id int,
	item_id int,
	nit_cliente varchar(9) not null,
	fecha timestamp default current_timestamp,
	calificacion int,
	foreign key (empleado_id) references empleado(empleado_id),
	FOREIGN KEY (item_id) REFERENCES items(item_id),
	foreign key (nit_cliente) references cliente(nit)
)

select * from items;

INSERT INTO empleado (nombre_empleado, contrasena_hash, rol, area_asignada) VALUES
('Juan Pérez', 'contrasena_juan', 'Camarero', 'Salón Principal'),
('María García', 'contrasena_maria', 'Camarero', 'Terraza'),
('Luis Martinez', 'contrasena_luis', 'Camarero', 'Jardín'),
('Ana Rodríguez', 'contrasena_ana', 'Camarero', 'Salón principal'),
('Carlos López', 'contrasena_carlos', 'Camarero', 'Barra'),
('Laura Fernandez', 'contrasena_laura', 'Gerente', 'Salón principal'),
('Javier Ruiz', 'contrasena_javier', 'Camarero', 'Terraza'),
('Sofía Gómez', 'contrasena_sofia', 'Camarero', 'Área VIP'),
('Diego Hernández', 'contrasena_diego', 'Camarero', 'Zona Lounge'),
('Andrea Díaz', 'contrasena_andrea', 'Camarero', 'Salón Principal');


CREATE TABLE mesas_unidas(
	id_unidad int PRIMARY KEY,
	id_cuenta INT,
	no_mesa1 INT, 
	no_mesa2 INT,
	id_area INT
)

ALTER TABLE mesas_unidas
ADD CONSTRAINT id_cuneta_fk FOREIGN KEY (id_cuenta) REFERENCES cuenta(id_cuenta);

ALTER TABLE mesas_unidas
ADD CONSTRAINT no_mesa1_fk FOREIGN KEY (no_mesa1) REFERENCES mesa(no_mesa);

ALTER TABLE mesas_unidas
ADD CONSTRAINT no_mesa2_fk FOREIGN KEY (no_mesa2) REFERENCES mesa(no_mesa);


ALTER TABLE mesas_unidas
ADD CONSTRAINT id_area_fk FOREIGN KEY (id_area) REFERENCES area(area_id);

CREATE OR REPLACE FUNCTION check_mesa_estado()
RETURNS TRIGGER AS $$
DECLARE
    area1 INT;
    area2 INT;
BEGIN
    -- Obtener el area_id de cada mesa
    SELECT area_id INTO area1 FROM mesa WHERE no_mesa = NEW.no_mesa1;
    SELECT area_id INTO area2 FROM mesa WHERE no_mesa = NEW.no_mesa2;

    -- Verificar si las mesas están en la misma área
    IF area1 IS NULL OR area2 IS NULL OR area1 <> area2 THEN
        RAISE EXCEPTION 'Las mesas % y % no están en la misma área', NEW.no_mesa1, NEW.no_mesa2;
    END IF;

    -- Verificar el estado y unida de no_mesa1
    IF NOT EXISTS (
        SELECT 1 FROM mesa
        WHERE no_mesa = NEW.no_mesa1 AND estado = FALSE AND unida = FALSE
    ) THEN 
        RAISE EXCEPTION 'La mesa % no está disponible para unirse', NEW.no_mesa1;
    END IF;

    -- Verificar el estado y unida de no_mesa2
    IF NOT EXISTS (
        SELECT 1 FROM mesa
        WHERE no_mesa = NEW.no_mesa2 AND estado = FALSE AND unida = FALSE
    ) THEN 
        RAISE EXCEPTION 'La mesa % no está disponible para unirse', NEW.no_mesa2;
    END IF;

    -- Actualizar el estado y unida de no_mesa1
    UPDATE mesa SET
        estado = TRUE,
        unida = TRUE
    WHERE no_mesa = NEW.no_mesa1;

    -- Actualizar el estado y unida de no_mesa2
    UPDATE mesa SET
        estado = TRUE,
        unida = TRUE
    WHERE no_mesa = NEW.no_mesa2;

    -- Si todo está correcto, permitir la inserción
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER before_insert_mesas_unidas
BEFORE INSERT OR UPDATE ON mesas_unidas
FOR EACH ROW EXECUTE FUNCTION check_mesa_estado();