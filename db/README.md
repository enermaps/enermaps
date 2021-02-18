# Database for the enermaps project

We use postgresql with postgis. The initial database schema 
can be found in db/add_dataset_db.sql

The sql schema will be loaded only if the `db-data` volume is not already present.
You can use `docker-compose down --volumes` and docker volume rm db-data` before running the app to load the schema and start from an empty db.

You can have an interactive session connected to psql with:

```
docker exec -it enermaps_db_1 psql -h 127.0.0.1 -p 5432 -U dataset dataset
```

## Sample queries

- Vector dataset, here with `ds_id = 2`

```
SELECT data."FID",
		json_object_agg(variable, value),
		fields,
		time, dt, z, data.ds_id, metadata, geometry
       FROM data
INNER JOIN spatial ON data."FID" = spatial."FID"
INNER JOIN datasets ON data.ds_id = datasets.ds_id
WHERE data.ds_id = 2
GROUP BY data."FID", time, dt, z, data.ds_id, fields, geometry, metadata
ORDER BY data."FID";
```
The pivoted table (variables + values to display on the map) is encapsulated as JSON in the `json_object_agg` column.


- Administrative units, here with `LEVL_CODE = NUTS1`

```
SELECT * FROM spatial WHERE "LEVL_CODE" = 'NUTS1';
```