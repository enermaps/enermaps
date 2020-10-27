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

You should then be able to run main.py for running the webserver locally or test.py for running all tests.

# Linting

We run black on version 20.8b1.
We advise you to run isort to take care of the order of dependencies.
