enermaps2 is a rewrite of the hotmaps poc based on the previous experience.

# frontend

app
Run it:
```
docker build -t frontend . && docker run -p 127.0.0.1:8000:80 frontend
```

then accessed trough http://127.0.0.1:8000

# api

```
docker build -t api . && docker run -p 127.0.0.1:8000:80 api
```
then accessed trough http://127.0.0.1:8000

# db
Currently a Work in progress
