database for the enermaps2 project.

We use postgresql with postgis. The initial database schema 
can be found in db/add_dataset_db.sql

You can have an interactive session connected to psql with:

```
docker exec -it enermaps2_db_1 psql -h 127.0.0.1 -p 5432 -U dataset dataset
```
