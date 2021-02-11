# Database for the enermaps project

We use postgresql with postgis. The initial database schema 
can be found in db/add_dataset_db.sql

The sql schema will be loaded only if the `db-data` volume is not already present.
You can use `docker-compose down --volumes` and docker volume rm db-data` before running the app to load the schema and start from an empty db.

You can have an interactive session connected to psql with:

```
docker exec -it enermaps_db_1 psql -h 127.0.0.1 -p 5432 -U dataset dataset
```
