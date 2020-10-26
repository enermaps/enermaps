enermaps2 is a rewrite of the hotmaps poc based on the previous experience.

# Run a local copy
run a 

```
docker-compose up --build
```
You can then access:

* the frontend on http://127.0.0.1:7000
* the api on http://127.0.0.1:7000/api

# frontend

app

then accessed trough http://127.0.0.1:8000

# api

You can also run the debug server with 

```
python api/main.py
```
and access it trough http://127.0.0.1:5000

# db

Database initialisation schema is ran when no previous data schema is found upon starting the db image.

You can access the database trough 127.0.0.1:5433
