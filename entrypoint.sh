#!/bin/bash

set -e

# Check that all required environment variables are set
if [ -z "$POSTGRES_USER" ] || [ -z "$POSTGRES_PASS" ] || [ -z "$POSTGRES_DBNAME" ] || [ -z "$POSTGRES_HOST" ] || [ -z "$POSTGRES_PORT" ]; then
   echo "Error: One or more required environment variables are not set."
   exit 1
fi

# echo out postgres env vars
echo "POSTGRES_USER: $POSTGRES_USER"
echo "POSTGRES_PASS: $POSTGRES_PASS"
echo "POSTGRES_DBNAME: $POSTGRES_DBNAME"
echo "POSTGRES_HOST: $POSTGRES_HOST"
echo "POSTGRES_PORT: $POSTGRES_PORT"


echo "CREATE EXTENSION IF NOT EXISTS postgis;" > /tmp/install_postgis_extension.sql
PGPASSWORD="$POSTGRES_PASS" psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DBNAME" -f /tmp/install_postgis_extension.sql
echo "PostGIS extension installation complete."

cat << EOF > setup-database.py
import os

from flask_cli import FlaskGroup
from flask_cors import CORS
from flask_migrate import Migrate

from app import blueprint
from app.main import create_app, db

app = create_app()
app.register_blueprint(blueprint)
app.app_context().push()
CORS(app, resources={r"/*": {"origins": "*"}})
cli = FlaskGroup(app)

migrate = Migrate()
migrate.init_app(app, db)
FLASK_APP = "manage.py"
db.create_all()
print("Database tables created")
EOF

FLASK_APP=manage.py python3 setup-database.py
rm setup-database.py

# FLASK_APP=manage.py python3 manage.py db migrate
# FLASK_APP=manage.py python3 manage.py db upgrade

echo "PostgreSQL database initialization complete."
exec "$@"