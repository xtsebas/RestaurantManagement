const { Pool } = require('pg');

// Configura la conexión a tu base de datos PostgreSQL
const pool = new Pool({
  user: 'tu_usuario',
  host: 'tu_host',
  database: 'tu_basededatos',
  password: 'tu_contraseña',
  port: tu_puerto, // El puerto por defecto de PostgreSQL es 5432
});

// Ejemplo de consulta a la base de datos
pool.query('SELECT NOW()', (err, res) => {
  if (err) {
    console.error('Error en la consulta:', err);
  } else {
    console.log('Resultado de la consulta:', res.rows[0]);
  }
  
  // Cierra la conexión después de usarla
  pool.end();
});
