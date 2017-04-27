FROM postgres:9.6

RUN mkdir -p /tmp/psql_data

COPY infra/db_ddl.sql /tmp/psql_data/
COPY infra/aa-init-docker-postgres.sh /docker-entrypoint-initdb.d/
