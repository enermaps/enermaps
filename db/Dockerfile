FROM camptocamp/postgres:9.6
ENV POSTGRES_USER test
ENV POSTGRES_DB test
RUN chmod 1777 /tmp # needed since July 2021 to be run on an Ubuntu 20.04.3 LTS server
ADD postgresql.conf /.
RUN chown -R postgres:postgres /postgresql.conf
ADD init/add_dataset_db.sql /docker-entrypoint-initdb.d/add_dataset_db.sql
ADD init/postgrest.sql /docker-entrypoint-initdb.d/postgrest.sql
