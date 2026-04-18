#!/bin/bash
# creating a databse for the bus system project 
# this is postegresql database
# the database name is bus_system_db
# the username is operator
# the password is passcode

# connect to the postgres database
psql -U postgres -c "CREATE DATABASE bus_system_db;"

# check is it is created
psql -U postgres -c "\l"
echo "the database is created successfully"

# create a user for the database
psql -U postgres -c "CREATE USER operator WITH PASSWORD 'passcode';"

# grant all privileges to the user on the database
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE bus_system_db TO operator;"

# check if the user is created
psql -U postgres -c "\du"
echo "the user is created successfully and granted privileges on the database"

# connect to the database using the new user
psql -U operator -d bus_system_db -c "\c"
echo "connected to the database successfully with the new user"

# create tables using schema.sql file
psql -U operator -d bus_system_db -f schema.sql
echo "tables created successfully using schema.sql file"

