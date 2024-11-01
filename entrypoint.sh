#!/bin/bash
# entrypoint.sh

# Wait for MySQL to be ready
echo "Waiting for MySQL..."
while ! mysqladmin ping -h"$MYSQL_HOST" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" --silent; do
    sleep 1
done
echo "MySQL is up and running."

# Create the database if it doesn't exist
echo "Creating database if not exists..."
mysql -h "$MYSQL_HOST" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS $MYSQL_DATABASE;"

# Create the db_version table if it doesn't exist and insert the initial value
echo "Creating db_version table and inserting initial value..."
mysql -h "$MYSQL_HOST" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -D "$MYSQL_DATABASE" -e "
CREATE TABLE IF NOT EXISTS db_version (
    version INT NOT NULL
);
INSERT INTO db_version (version) 
SELECT 0 FROM DUAL 
WHERE NOT EXISTS (SELECT 1 FROM db_version);
"

echo "Starting Flask APP..."
# Start Flask
rococo-mysql --migrations-dir=./common/migration  --env-files=.env rf
exec python flask/app.py
