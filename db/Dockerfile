FROM camptocamp/postgres:9.6
# RUN rm -r /var/lib/postgresql/data/*
ENV POSTGRES_USER test
ENV POSTGRES_DB test
ADD add_dataset_db.sql /docker-entrypoint-initdb.d/add_dataset_db.sql
