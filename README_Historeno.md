# Run the services

## Run Historeno platform
```
docker-compose --file docker-compose-historeno.yml up --build
```

# CM Historeno

## Service
service name : cm-historeno

# Database

## Service
service name : db

## Modification from EmerMaps
added variable environment in the docker-compose :
```yml
PGDATA: /var/lib/postgresql/data/historeno
```

## pgAdmin acess

```markdown
host : 127.0.0.1
Port : 5433
Maintenance database : postgres
Username : test (or see .env-db)
DB_PASSWORD : example (or see .env-db)
```

# Postgrest
## Service
## Modification from EmerMaps
- add .postgrest file
```
PGRST_DB_URI=postgres://test:example@db:5432/dataset
PGRST_DB_ANON_ROLE=api_anon
PGRST_JWT_SECRET={PASSWORD}
```


# Part
## Service
## Modification from EmerMaps
