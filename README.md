# Sistema de Gestión de Restaurante

## Descripción
Este proyecto es un sistema de gestión para un restaurante. Permite a los empleados, como meseros y administradores, realizar diversas tareas, como tomar pedidos, gestionar mesas, generar facturas y más.

## Características principales
- **Inicio de sesión seguro:** Los usuarios pueden iniciar sesión utilizando su nombre de usuario y contraseña, que se almacenan de manera segura utilizando el algoritmo bcrypt para el hash de contraseñas.
- **Gestión de mesas:** Los meseros pueden asignar mesas a los clientes, tomar pedidos y cerrar cuentas cuando los clientes terminan de comer.
- **Toma de pedidos:** Los meseros pueden registrar los pedidos de los clientes, especificando los platos y la cantidad deseada.
- **Facturación:** El sistema genera facturas detalladas para cada mesa, incluyendo el total de la cuenta, propina y total final.
- **Seguimiento de empleados:** Los administradores pueden supervisar las actividades de los empleados, incluyendo la amabilidad y exactitud del servicio.
- **Interfaz intuitiva:** La interfaz de usuario está diseñada para ser fácil de usar tanto para los empleados como para los clientes.

## Utilizacion de archivos
- El archivo restaurante.py es el principal, ya que es el manejador de todo el codigo en general
- controller.py contiene funciones en base de datos, al igual que db_test1.py, solo que este archivo tiene la conexion directa a la base de datos
- project2.sql es el codigo original para generacion de las tablas, al igual que sus triggers.
- ER.png es el modelo ER en el que se baso para crear todo el proyecto

