## CM

Create the new file for the new cm

Implement new cm in this file 
which would post the result (a raster) on the api.

## Requirements

Add all the requirements in the requirements.txt file

## Dockerfile

Use the same docker file :

```
FROM ubuntu:20.04
RUN apt-get update && \
    apt-get --yes install python3 python3-pip &&\
    rm -rf /var/cache/apt/archives/
WORKDIR cm-[cm file name]
COPY [cm file name]/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY base /tmp/base
RUN cd /tmp/base && pip3 install . && python3 test.py
COPY [cm file name] .
RUN python3 test.py
CMD ["python3", "worker.py"]
```

## Docker-compose

Add new service :

```
cm-[name of the cm]:
  build:
    context: ./cm
    dockerfile: [name of the cm file]/Dockerfile
  environment:
    UPLOAD_DIR: /upload-dir
  volumes:
    - upload-data:/upload-dir
```

## Test

Create test in a test.py file

Example of empty test :

```python
import unittest


if __name__ == "__main__":
    unittest.main()

```

## Json schema

Add an empty json schema in the schema.json file :

```
{
}
```

## Linter

Set the linter parameters in the setup.cfg file :

```
[flake8]
max-line-length=88
[isort]
line_length=88
```

Must be the same than others setup file
