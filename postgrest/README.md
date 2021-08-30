# Postgrest API

This services provides a Postgrest API access to the DB.

The service needs the following `.postgrest` envinronment file to be placed in the root directory (the same as the `docker-compose_db.yml`):

```
PGRST_DB_URI=postgres://test:example@db:5432/dataset
PGRST_DB_ANON_ROLE=api_anon
PGRST_JWT_SECRET={PASSWORD}
```
where `{PASSWORD}` is a secret password.
You can generate one with:
```bash
# Allow "tr" to process non-utf8 byte sequences
export LC_CTYPE=C

# read random bytes and keep only alphanumerics
< /dev/urandom tr -dc A-Za-z0-9 | head -c32
```

## Preparing the DB
The API users and custom functions are initialized in the db service.
If you don't want to rebuild the db, you can just execute postgrest custom sql:

```
docker-compose -f docker-compose_db.yml up --build -d db
docker-compose exec db psql postgres://test:example@db:5432/dataset -f /docker-entrypoint-initdb.d/postgrest.sql
```

## Usage

Run the service:
```
docker-compose up --build -d postgrest
```

You should see the API on:
http://localhost:3000

Sample request using Python:

```python
import requests
API_KEY = {API_KEY}
r = requests.get('http://localhost:3000/datasets',
	headers={'Authorization': 'Bearer {}'.format(API_KEY)})
response = r.json()
print(response)
```
where the `{API_KEY}` is the signed token created with the password. See [here](https://postgrest.org/en/v7.0.0/tutorials/tut1.html) for a tutorial.

The payload should include the `api_user`:

```javascript
{
  "role": "api_user",
}
```

Sample query returning all records of a given dataset as a GeoJSON:
```python
r = requests.post('http://localhost:3000/rpc/enermaps_query_geojson',
	headers={'Authorization': 'Bearer {}'.format(API_KEY)},
	json={"parameters": {"data.ds_id": 2})
response = r.json()
print(response)
```
This is based on the PostgreSQL function `enermaps_geojson()`.

To prevent large queries, these optional parameters are set by default:

- `row_limit = 100`
- `row_offset = 0`

More complex queries can be composed using the `enermaps_query_geojson endpoint`, e.g.:
```python
	json={"parameters" : {"data.ds_id": "2", "fields": {"min_temp": "240", "max_temp": "310"}}}
```

**IMPORTANT**
After adding/updating functions, you need to rebuild Postgrest cache using the following command:

```docker-compose kill -s SIGUSR1 postgrest```

### Retrieving administrative units
To filter administrative units, the `level` parameter can be used.
The available options are: `country`, `NUTS1`, `NUTS2`, `NUTS3`, `LAU`.

Example for `NUTS1`:
```python
r = requests.post('http://localhost:3000/rpc/enermaps_query_geojson',
	headers={'Authorization': 'Bearer {}'.format(API_KEY)},
	json={"parameters": {"data.ds_id": 0, "level": "{NUTS1}"}})
response = r.json()
```
Multiple options can be included, separated with a comma, e.g. `"level": "{NUTS1,NUTS2}"`
By default all levels are queried, including the level `geometry`, which corresponds to custom geometries (e.g. points of power plants).


## Gateway API - WIP
Here are the first steps towards an API linking EnerMaps EDMT to OpenAIRE Gateway.

### Metadata table
We create a table named `datasets_full` which contains the metadata records of all 50 datasets.
```sql
-- Code to support OPENAIRE gateway
-- Create a new datasets table to be filled in
-- as the original datasets table only contains integrated datasets
CREATE TABLE public.datasets_full
(
    ds_id int PRIMARY KEY,
    shared_id varchar(200),
    metadata json
);
GRANT SELECT ON public.datasets_full TO api_user;
-- Make it public to anynomous users
GRANT SELECT ON public.datasets_full TO api_anon;
```
This is provisional, waiting for the `datasets` table to be filled in with all datasets and to avoid conflicts with data-integration during development.
WARNING: Unlike the other tables, it is public.

We can populate it using:

```
docker-compose -f docker-compose_db.yml up --build -d data-integration && docker-compose -f docker-compose_db.yml exec data-integration python3 addDatasets.py
```

### Available endpoints
Here are some sample requests to be adapted for OpenAIRE support.

#### Sample filtering using GET
http://localhost:3000/datasets_full?shared_id=eq.jrc-10128-10001

#### Custom query using POST
```python
r = requests.post('http://localhost:3000/rpc/enermaps_get_metadata',
	headers={'Authorization': 'Bearer {}'.format(API_KEY)},
	json={"shared_id": "jrc-10128-10001"})
response = r.json()
print(response)
```

#### Datacite view using GET
A custom view has been created to provide an endpoint for OpenAIRE aggregator and list all records using the[Datacite schema](https://support.datacite.org/docs/api-get-lists).
This is available on: http://localhost:3000/datacite

By default, the PostgREST view results in [an array](https://postgrest.org/en/v7.0.0/api.html#singular-or-plural).
To change the behavior and return a JSON object, we can add a specification in the header:

```python
r = requests.get('http://localhost:3000/datacite',
	headers={'Accept': 'application/vnd.pgrst.object+json'})
response = r.json()
print(json.dumps(response,indent=4, sort_keys=True))
```

#### Metadata view using GET
A custom view has been created to provide an endpoint for OpenAIRE and list all Enermaps-specific metadata.
This is available on: http://localhost:3000/metadata
