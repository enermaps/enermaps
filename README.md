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
* the database on 127.0.0.1:5433

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

## Cleanup

You can stop the entire stack with

```
docker-compose stop
```

You can remove all data and images, if for example you wanna start from scratch with:

```
docker-compose rm
docker volume prune
```

