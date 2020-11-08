Enermaps HTTP api.

This directory host the api for the enermaps project.

# Running locally

For running the api locally, the current recommended method 
is to use docker-compose (see the README at the root of the directory).

You can still run the api locally for developpement purpose. You will need

* python 3.6+
* pip
* mapnik version above 3.0

You can optionally create a virtual environment prior to running the install commands for installing the environment.

Then proceed to install the requirement with:

```
pip install -r requirements.txt
```

You should then be able to run main.py for running the webserver locally or test.py for running all tests using on unix platform:

```
python $(pwd)/main.py
```
The api will listen http://127.0.0.1:7000

# Linting

We run a series of linter which are listed in linter-requirements.txt with their version. 
You can run them locally by first installing them:

```
pip install -r linter-requirements.txt
```
They are:

* black for automated formatting
* bandit for security scanning

# acceptance test 

Currently, the wms_test/acceptance_test.py is testing for the initialisation of the wms library.
The script can be ran as a python script. It need the enermaps project to already be started and be reachable 
under the url URL.

You can then call the script with:

```
python wms_test/acceptance_test.py --url URL
```

You can also test for a specific wms version with 

```
python wms_test/acceptance_test.py --url URL --version 1.3.0
```
