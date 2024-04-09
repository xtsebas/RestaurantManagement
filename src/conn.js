const { Pool } = require('pg');

// Configura la conexión a tu base de datos PostgreSQL
const pool = new Pool({
  user: 'u9h73gvdn3nqqq',
  host: 'c7gljno857ucsl.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com',
  database: 'dbqa0v50s9e961',
  password: 'p3a93c7dd4442cdfc25db1687dadde248f90752ba646cd88e60fa4a95c3c119fd',
  port: 5432  , // El puerto por defecto de PostgreSQL es 5432
  ssl: {
    rejectUnauthorized: false
  }
});

export default pool;