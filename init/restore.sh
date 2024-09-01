#!/bin/bash
set -e

echo "Restoring database from dump file..."
pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" /docker-entrypoint-initdb.d/mydatabase.dump
echo "Database restored successfully!"