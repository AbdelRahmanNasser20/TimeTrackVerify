set -e

echo "Starting database initialization..."

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
    DROP DATABASE IF EXISTS mydatabase;
    CREATE DATABASE mydatabase;
    CREATE ROLE myuser WITH LOGIN PASSWORD 'mypassword';
    ALTER ROLE myuser WITH SUPERUSER;
EOSQL

echo "Database mydatabase created and role myuser added."

pg_restore -U "$POSTGRES_USER" -d mydatabase /docker-entrypoint-initdb.d/mydatabase.dump

echo "Database mydatabase restored."