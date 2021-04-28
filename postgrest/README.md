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
create role api_anon nologin;
grant usage on schema public to api_anon;
grant api_anon to test;

create role api_user nologin;
grant api_user to test;

grant usage on schema public to api_user;
grant select on public.spatial to api_user;
grant select on public.data to api_user;
grant select on public.datasets to api_user;
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
where the {API_KEY} is the signed token created with the password. See [here](https://postgrest.org/en/v4.1/tutorials/tut1.html#step-3-sign-a-token) for a tutorial.