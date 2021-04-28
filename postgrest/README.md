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
`
openssl rand -base64 32
`

## Preparing the DB
The API users are initialized in the db service.
You need then to recreate the db service with the following commands:
```
docker-compose down -v
docker volume rm enermaps_db-data 
docker-compose up --build -d db
```
Warning: the db will be initialized. You would probably need to re-integrate some datasets.

As an alternative, you can run this in psql:

```sql
CREATE ROLE api_anon nologin;
GRANT usage ON schema public TO api_anon;
GRANT api_anon TO test;

CREATE ROLE api_user nologin;
GRANT api_user TO test;

GRANT USAGE ON schema public TO api_user;
GRANT SELECT ON public.spatial TO api_user;
GRANT SELECT ON public.data TO api_user;
GRANT SELECT ON public.datasets TO api_user;
```

# Usage

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
where the `{API_KEY}` is the signed token created with the password. See [here](https://postgrest.org/en/v4.1/tutorials/tut1.html#step-3-sign-a-token) for a tutorial.

Sample query returning all records of a given dataset:
```python
r = requests.post('http://localhost:3000/rpc/enermaps_query',
	headers={'Authorization': 'Bearer {}'.format(API_KEY)},
	json={"ds_id": 2})
response = r.json()
print(response[:10]) # limit to the first 10
```
This is based on the PostgreSQL function `enermaps_query()`.