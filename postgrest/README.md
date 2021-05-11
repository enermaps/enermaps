# Postgrest API

This services provides a Postgrest API access to the DB.

The service needs the following `.postgrest` envinronment file to be placed in the root directory (the same as the `docker-compose.yml`):

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
docker-compose up --build -d db
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
  "user": "api_user",
}
```

Sample query returning all records of a given dataset as a GeoJSON:
```python
r = requests.post('http://localhost:3000/rpc/enermaps_geojson',
	headers={'Authorization': 'Bearer {}'.format(API_KEY)},
	json={"dataset_id": 2})
response = r.json()
print(response)
```
This is based on the PostgreSQL function `enermaps_geojson()`.

After adding/updating functions, you need to rebuild Postgrest cache using the following command:

```docker-compose kill -s SIGUSR1 postgrest```

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
docker-compose up --build -d data-integration && docker-compose exec data-integration python3 addDatasets.py
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
