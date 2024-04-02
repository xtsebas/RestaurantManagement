const { Client } = require('pg');

// Configura la conexión a tu base de datos PostgreSQL
const client = new Client({
  user: "u9h73gvdn3nqqq",
  password: "p3a93c7dd4442cdfc25db1687dadde248f90752ba646cd88e60fa4a95c3c119fd",
  host: "c7gljno857ucsl.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com",
  database: "dbqa0v50s9e961",
  port: 5432
});

// Conecta a la base de datos
client.connect()
  .then(() => console.log('Connected to PostgreSQL successfully'))
  .then(() => {
    // Ejecuta la consulta
    return client.query('SELECT * FROM items');
  })
  .then((result) => {
    console.log('Rows from query:');
    result.rows.forEach(row => {
      console.log(row);
    });
  })
  .catch(error => console.error('Error while connecting to PostgreSQL:', error))
  .finally(() => client.end()); 
