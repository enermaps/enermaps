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

You can also rebuild the set of all services, and docker will only rebuilt the
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

## Symlink on window

This repository was previously using symlinks to unify all the setup.cfg. On windows, this required sometimes administrative
rights (see https://github.community/t/git-bash-symbolic-links-on-windows/522), thus we manually updated each setup.cfg to
be the same. When updating one setup.cfg, you will need to be carefull to update all of them.


# Code structure with pre-commit, black, bandit, flake8, isort :

Setup your work environment:

```
# create a virtual environment
virtualenv env --python=python3 # or python3 -m venv env
# activate the virtual environment
source env/bin/activate
# install the requirements
pip install -r requirements.txt
# install pre-commit
pre-commit install
```

Work in that environment following this procedure:

 - When a git commit is done your code gets automatically re-formatted
 - You will have to check the proposed modifications and re-add them in a continuous process of `git add`/`git commit`
 - When your code passes the pre-commit checks, you will be able to finally commit your code and push to GitHub
 - Various imports are automatically sorted for you
 - Automatic checks verify that unused libraries and variables can't get committed
 - Contributors are expected to follow this code of conduct as it guarantees code formatting quality
