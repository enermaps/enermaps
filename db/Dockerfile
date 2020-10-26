FROM camptocamp/postgres:9.6

ENV POSTGRES_USER test
ENV POSTGRES_DB test
ADD *.sql /docker-entrypoint-initdb.d/
