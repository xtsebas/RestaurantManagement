import pool from "./conn";

async function getAllItems() {
    // Ejecutar consulta SQL para seleccionar todos los registros en la tabla anime
    const [rows] = await pool.query('SELECT * FROM empleado');
    return rows;
}

async function checkUserPassword(username, password) {
    try {
        // Ejecutar consulta SQL para seleccionar el empleado con el nombre de usuario dado
        const [rows] = await pool.query('SELECT * FROM empleado WHERE nombre_empleado = ?', [username]);
        
        // Verificar si se encontró un empleado con el nombre de usuario dado
        if (rows.length === 0) {
            // No se encontró ningún empleado con el nombre de usuario dado
            return { success: false, message: 'Usuario no encontrado' };
        }
        
        const empleado = rows[0];
        
        // Verificar si la contraseña coincide
        if (empleado.contrasena_hash !== password) {
            // La contraseña es incorrecta
            return { success: false, message: 'Contraseña incorrecta' };
        }
        
        // Las credenciales son correctas
        return { success: true, empleado };
    } catch (error) {
        // Error al ejecutar la consulta SQL
        console.error('Error al verificar las credenciales:', error);
        return { success: false, message: 'Error al verificar las credenciales' };
    }
}

export {checkUserPassword};