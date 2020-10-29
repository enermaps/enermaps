enermaps2 is a rewrite of the hotmaps poc based on the previous experience.

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
