#!/bin/bash
# creating a databse for the bus system project 
# this is postegresql database
# the database name is bus_system_db
# the username is operator
# the password is passcode

set -e

# Load from .env or use defaults
DB_NAME="${DB_NAME:-bus_system_db}"
DB_USER="${DB_USER:-operator}"
DB_PASSWORD="${DB_PASSWORD:-passcode}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCHEMA_FILE="$SCRIPT_DIR/schema.sql"

if [[ ! -f "$SCHEMA_FILE" ]]; then
    echo "Error: schema.sql not found at $SCHEMA_FILE"
    exit 1
fi

echo "Creating database: $DB_NAME on $DB_HOST:$DB_PORT"
psql -h "$DB_HOST" -U postgres -p "$DB_PORT" -c "CREATE DATABASE $DB_NAME;" || echo "Database may already exist"

echo "Creating user: $DB_USER"
psql -h "$DB_HOST" -U postgres -p "$DB_PORT" -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" || echo "User may already exist"

echo "Granting privileges..."
psql -h "$DB_HOST" -U postgres -p "$DB_PORT" -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

echo "Creating tables from schema..."
psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -p "$DB_PORT" -f "$SCHEMA_FILE"

echo "✓ Database setup completed successfully"
