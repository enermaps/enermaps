enermaps is a rewrite of the hotmaps poc based on the previous experience.

# Development
First you need to have docker installed on your machine.

Then run

```
docker-compose up --build
```
This will start the frontend, the api and the database

You can then access:

* the frontend on http://127.0.0.1:7000
* the api on http://127.0.0.1:7000/api
* the database is available on host 127.0.0.1 and port 5433 with the psql 
client (see ![](db/README.md))
* the broker (redis) is available on host 127.0.0.1 and port 6379 with a redis client.
* the broker can also be monitored trough http://127.0.0.1:5555, which is running flower, a monitoring interface for long running tasks.

The initial database schema will be created following the step in ![](db/README.md).

For updating a service, you will need to run:

```
docker-compose up --build -d $service
```

where service can be one of frontend, api or db.

You can also rebuild the set of all service, and docker will only rebuilt the 
changed images with the following command:

```
docker-compose up --build -d
```

Some service will initialize and create their initial state:

* the api will fetch an initial dataset
* the db will create its initial schema

## Cleanup

You can stop the entire stack with

```
docker-compose stop
```

You can remove all data and images, if for example you wanna start from scratch with:

```
docker-compose down -v
```

# Continuous Integration

We use [github actions](https://github.com/features/actions) for continuous integration on the project.
You can test those action locally using https://github.com/nektos/act. After having installed act, you can run

```
act pull_request
```

