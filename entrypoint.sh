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
## Clean up the temporary schema file
#rm /tmp/pgstac.sql
echo "CREATE EXTENSION IF NOT EXISTS postgis;" > /tmp/install_postgis_extension.sql
PGPASSWORD="$POSTGRES_PASS" psql -h "$POSTGRES_HOST_WRITER" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DBNAME" -f /tmp/install_postgis_extension.sql

cat << EOF > setup.py
import os

from flask_cli import FlaskGroup
from flask_cors import CORS
from flask_migrate import Migrate

from app import blueprint
from app.main import create_app, db
db.create_all()
EOF

FLASK_APP=manage.py python3 setup.py

# FLASK_APP=manage.py python3 manage.py db migrate
# FLASK_APP=manage.py python3 manage.py db upgrade

echo "PostgreSQL database initialization complete."
exec "$@"