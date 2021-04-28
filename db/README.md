# Database for the enermaps project

We use postgresql with postgis. The initial empty database schema can be found in db/add_dataset_db.sql

The sql schema will be loaded only if the `db-data` volume is not already present.
As a reminder, you would need to execute a `docker-compose down --volumes` before running the app to load the schema and start from an empty db.

You can have an interactive session connected to psql with:

```
docker exec -it enermaps2_db_1 psql -h 127.0.0.1 -p 5432 -U dataset dataset
```

## Sample queries

- Vector dataset, e.g `ds_id = 2`

```sql
SELECT data.fid,
		json_object_agg(variable, value),
		fields,
		start_at, dt, z, data.ds_id, metadata, geometry
       FROM data
INNER JOIN spatial ON data.fid = spatial.fid
INNER JOIN datasets ON data.ds_id = datasets.ds_id
WHERE data.ds_id = 2
GROUP BY data.fid, start_at, dt, z, data.ds_id, fields, geometry, metadata
ORDER BY data.fid;
```

The pivoted table (variables + values to display on the map) is encapsulated as JSON in the `json_object_agg` column.


- Administrative units, here with `levl_code = NUTS1`

```sql
SELECT * FROM spatial WHERE "levl_code" = 'NUTS1';
```

- Raster dataset, e.g. `ds_id = 43`
The same query as for a vector dataset can be used. The name of the raster file to be loaded is set in the `FID` field. The complete path of each raster file can be constructed as follows:
`di/data/{ds_id}/{FID}`