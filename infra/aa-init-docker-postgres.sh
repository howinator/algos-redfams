#!/usr/bin/env bash
# Named aa-* so that it runs first in docker start-up (run alphabetically)
set -ex

DB_NAME='algosreddit'
DB_DDL_LOCATION='/tmp/psql_data/db_ddl.sql'

psql -v ON_ERROR_STOP=1 --username "postgres" <<-EOSQL
    CREATE DATABASE "$DB_NAME";
    GRANT ALL PRIVILEGES ON DATABASE "$DB_NAME" TO postgres;
EOSQL

psql --username="postgres" --dbname="$DB_NAME" -a -f "$DB_DDL_LOCATION"
