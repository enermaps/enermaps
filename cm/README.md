Base directory for the calculation modules (cm).

A calculation module is an asynchronous slow task (from seconds to hours of latency for the answer). 
A calculation module takes a set of raster, a selection and an optional set of parameters

# Create a new cm

Each calculation module is a subdirectory in this directory.

It must contain:
* A setup.cfg symlink to the cm/setup.cfg file. (see
  https://mokacoding.com/blog/symliks-in-git/ for a brief explanation on symbolic links)
* A worker.py entrypoint, this must be an executable that start the worker.
* A test.py unittest testing the calculation without service dependencies (see 
  https://docs.python.org/3/library/unittest.html for explination about unittest library).
* A schema.json jsonschema which describes the schema used for the input. 
  You can find additional information about jsonschema
  (see https://json-schema.org/).
* A requirements.txt including cm specific dependencies.
* A Dockerfile to create the necessary docker image.
  The docker-compose will need to be modified accordingly to create the new image.
* A python script relating to the cm code.
* A readme file describing the cm operation.

Below is an example of the tree structure :

```bash
─── cm
    └── first_cm
        ├── setup.cfg
        ├── worker.py
        ├── test.py
        ├── schema.json
        ├── requirements.txt
        ├── Dockerfile
        ├── new_cm.py
        └── README.md
```


## Setup.cfg

Below is the setup file configuration.

```
[flake8]
max-line-length=88
[isort]
line_length=88
```

To keep consistency in the project, 
the following parameters mustn't be changed.

## Worker.py

Below is an example of the broker implementation.

````python
#!/usr/bin/env python3
import BaseCM.cm_base as cm_base

from new_cm import process


app = cm_base.get_default_app()
schema_path = cm_base.get_default_schema_path()


@app.task(base=cm_base.CMBase, bind=True, schema_path=schema_path)
def fun(self, selection: dict, rasters: list, params: dict):
    """New cm description"""
    result = process(selection, rasters, params)
    return result


if __name__ == "__main__":
    cm_base.start_app(app)
````

The selected area and the selected raster 
are in the variable ```selection``` and ```rasters``` respectively.

The variable ```params``` refers to the data provided by the form on the frontend.

## Test.py

Below is an example of cm test.

```python
import unittest

from new_cm import process

selection = "selection.shp"
raster = "raster.tif"
params = 10

class TestNewCM(unittest.TestCase):
    def test_new_cm_feature(self):
        result = process(selection, rasters, params)
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
```

## Schema.json

Below is an example of the data schema expected by the cm.

```
{
  "type": "object",
  "properties": {
    "factor": {
      "type": "number",
      "default": 1
    }
  }
}
```

## Requirements.txt

Below is an example of the dependencies used by a cm.

```
lxml==4.6.2
GDAL==3.0.4
```

Only the dependencies specific to the cm are to be mentioned in the requirements.txt.

The dependencies below will be available for all cm.

````
marshmallow==3.9.1
marshmallow-union==0.1.15.post1
jsonschema==3.2.0
celery==5.0.2
redis==3.5.3
requests
````

Whenever possible, it is preferable to specify 
the version of the dependency used. 

## Docker

### Dockerfile

Below is an example of a Dockerfile

```
FROM ubuntu:20.04
RUN apt-get update && \
    apt-get --yes install python3 python3-pip &&\
    rm -rf /var/cache/apt/archives/
WORKDIR cm-first_cm
COPY first_cm/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY base /tmp/base
RUN cd /tmp/base && pip3 install . && python3 test.py
COPY first_cm .
RUN python3 test.py
CMD ["python3", "worker.py"]
```

### Docker-compose

After adding those entrypoint, you can add your calculation module in the docker-compose.yml file at the root of this directory.


Below is an example of the creation of the new service.

```
cm-first_cm:
  build:
    context: ./cm
    dockerfile: first_cm/Dockerfile
  environment:
    UPLOAD_DIR: /upload-dir
  volumes:
    - upload-data:/upload-dir
  env_file:
    .env
```

# Test a cm

Currently to test a particular cm, you will need to first start enermaps using docker-compose up in the root directory.
Then you can connect to the redis queue. The multiply cm is given as an example.

We strongly encourage you to write unittest that verify the good working of a calculation module separated from the enermaps api.

# CMs interaction

Currently, the cm registers on the redis queue trough the celery library.
An helper library is given, you can find it under base/BaseCM/ and an example is given in
multiply/
