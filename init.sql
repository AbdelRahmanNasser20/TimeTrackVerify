-- Connect to the default postgres database to run commands
\c postgres

-- Drop and recreate the target database
DROP DATABASE IF EXISTS mydatabase;
CREATE DATABASE mydatabase;

-- Connect to the new database
\c mydatabase

-- Restore the dump file into the new database
\i /docker-entrypoint-initdb.d/mydatabase.dump