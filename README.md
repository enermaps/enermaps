The EnerMaps project has received funding from the European Union’s Horizon 2020 research and innovation program under grant agreement N°884161.

EnerMaps is a rewrite of Hotmaps Horizon 2020 project.

# Development
First you need to have docker installed on your machine.
Clone this repository.

Then run

```
docker-compose up --build
```
This will start the frontend and the api.

Run

```
docker-compose --file docker-compose-db.yml up --build
```

to start the database.

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

where service can be one of frontend or api. To update the db, run

```
docker-compose --file docker-compose-db.yml up --build -d db
```

You can also rebuild the set of all services, and docker will only rebuilt the
changed images with the following command:

```
docker-compose up --build -d
```

or

```
docker-compose --file docker-compose-db.yml up --build -d
```

for the db.

Some services will initialize and create their initial state:

* the api will fetch an initial dataset
* the db will create its initial schema

## Data-integration

To import datasets, check the data-integration directory readme.

## Populating the WMS cache

For the WMS to work, geofiles must be downloaded from the database server:

```
$ docker-compose exec api /bin/bash -c 'flask update-areas'

$ docker-compose exec api /bin/bash -c 'flask list-datasets'
- 1: PVGIS: Solar Radiation Data (raster)
- 2: JRC: Geothermal Power Plant Dataset (vector)
- 3: JRC: Hydro-power plants database (vector)
- 4: JRC: Open Power Plants Database (vector)
...

$ docker-compose exec api /bin/bash -c 'flask update-dataset 3'
```

Note that by default, the `update-dataset` command will respect the default area
defined for the dataset in the database server. This is mainly for development
purposes, as those datasets have GB of data and you only need a subset to work on
them. To download all the dataset, use the `--all` option:

```
$ docker-compose exec api /bin/bash -c 'flask update-dataset --all 35'
```

On the production server, to populate the WMS cache with all the available
datasets, do:

```
$ docker-compose exec api /bin/bash -c 'flask update-all-datasets'
```

## External API

A PostGREST API is available to give access to the DB to external users, as well as to the OpenAIRE gateway.

Check the the PostGREST directory readme.

### Nginx server

The Nginx service manages different endpoints to provide access to the:

- the PostGREST API
- the raster files
- custom thumbnail pictures for OpenAIRE gateway.

Check the the nginx directory readme.

## Cleanup

You can stop the entire stack with

```
docker-compose stop
```

You can remove all data and images, if for example you want to start from scratch with:

```
docker-compose down --volumes --remove-orphans
```

# Continuous Integration

We use [github actions](https://github.com/features/actions) for continuous integration on the project.
You can test those action locally using https://github.com/nektos/act. After having installed act, you can run

```
act pull_request
```

## Symlink on window

This repository was previously using symlinks to unify all the setup.cfg. On windows, this required sometimes administrative
rights (see https://github.community/t/git-bash-symbolic-links-on-windows/522), thus we manually updated each setup.cfg to
be the same. When updating one setup.cfg, you will need to be carefull to update all of them.


# Linting

We run a series of linters which are listed in linter-requirements.txt with their version.

You can either run them manually, automatically each time you do a commit, or both.


## Manual linting

You can install the linting tools by doing:

```
pip install -r linter-requirements.txt
```

They are:

* black for automated formatting
* bandit for security scanning
* isort for the order of the import
* flake8 for line length, unused variable and others.


## Automatic linting at each commit

Setup your work environment:

```bash
# create a virtual environment
virtualenv env --python=python3 # or python3 -m venv env
# activate the virtual environment
source env/bin/activate
# install the requirements
pip install -r precommit-requirements.txt
# nodejs will be in the python env
nodeenv --python-virtualenv
# install npm packages
npm install eslint@7.32.0
npm install eslint-config-google
npm install eslint-plugin-svelte3
# install pre-commit
pre-commit install
```

Work in your environment following this procedure:

 - When a git commit is done, your code gets automatically re-formatted
 - You will have to check the proposed modifications and re-add them in a continuous process of `git add`/`git commit`
 - When your code passes the pre-commit checks, you will be able to finally commit your code and push to GitHub
 - Various imports are automatically sorted for you
 - Automatic checks verify that unused libraries and variables can't get committed
 - Contributors are expected to follow this code of conduct as it guarantees code formatting quality

## Documentation Platform

Creating a thorough documentation for this project is an essential task. To facilitate this, a dedicated platform has been composed. The source code and detailed description of the platform can be found in the [doc](./doc) module of this repository.

### Who can contribute to the project documentation?

All the GitHub users who are either collaborators or contributors in the enermaps/doc repository can login on the web platform with their GitHub user name or email address and are authorized to modify the docs.

**Note that it is not sufficient to simply have read / write access in the enermaps/doc repository to be authorized for content editing. A user should be added to the list of collaborators explicitly, or should contribute to some branch of the repo with at least one commit.**

### Building the platform

All the environment variable values should be added to `.env-doc`, then the service can be built and ran using the following commands:

```shell
docker-compose --file docker-compose-doc.yml build
docker-compose --file docker-compose-doc.yml up -d
```
