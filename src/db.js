import pool from './conn.js';

async function getAllItems() {
    try {
        const result = await pool.query('SELECT * FROM items');
        const rows = result.rows; 
        console.log('Filas obtenidas:', rows); 
        return rows;
    } catch (error) {
        console.error('Error al obtener items:', error);
        throw error;
    }
}

async function getEmployees(name, password) {
    try {
        const result = await pool.query('SELECT * FROM empleado WHERE nombre_empleado = $1 AND contrasena_hash = $2', [name, password]);
        const rows = result.rows; 
        if (rows.length === 0) {
            throw new Error('Empleado no encontrado o la contraseña es incorrecta');
        }
        console.log('Filas obtenidas:', rows); 
        return rows;
    } catch (error) {
        console.error('Error al obtener items:', error);
        throw error;
    }
}

export {getAllItems, getEmployees};