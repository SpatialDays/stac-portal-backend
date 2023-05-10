#!/bin/bash

set -e

## Check that all required environment variables are set
#if [ -z "$POSTGRES_USER" ] || [ -z "$POSTGRES_PASS" ] || [ -z "$POSTGRES_DBNAME" ] || [ -z "$POSTGRES_HOST_WRITER" ] || [ -z "$POSTGRES_PORT" ]; then
#    echo "Error: One or more required environment variables are not set."
#    exit 1
#fi

## Download the schema file from the provided URL
#wget -O /tmp/pgstac.sql https://raw.githubusercontent.com/stac-utils/pgstac/main/src/pgstac/migrations/pgstac.0.7.1.sql
#
## Connect to the database and initialize it with the schema
#PGPASSWORD="$POSTGRES_PASS" psql -h "$POSTGRES_HOST_WRITER" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DBNAME" -f /tmp/pgstac.sql
## Clean up the temporary schema file
#rm /tmp/pgstac.sql


FLASK_APP=manage.py python3 manage.py db migrate
FLASK_APP=manage.py python3 manage.py db upgrade

echo "PostgreSQL database initialization complete."
exec "$@"