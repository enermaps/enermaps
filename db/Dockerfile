FROM camptocamp/postgres:9.6
ENV POSTGRES_USER test
ENV POSTGRES_DB test
ADD init/add_dataset_db.sql /docker-entrypoint-initdb.d/add_dataset_db.sql
ADD init/postgrest.sql /docker-entrypoint-initdb.d/postgrest.sql
