# nginx

This service exposes:
 - thumbnail pictures representing each dataset `0.0.0.0/images/{shared_id}`
 - the raster files `0.0.0.0/raster/{ds_id}/{fid}`

It also acts as reverse-proxy by redirecting calls to `0.0.0.0/api` to the PostgREST API.

The address scheme is tested to work on the enermaps server.
