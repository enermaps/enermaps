# nginx

This services exposes thumbnail pictures representing each dataset, which will be displayed in the OpenAIRE gateway.

It also acts as reverse-proxy by redirecting calls to `127.0.0.1/api` to the PostgREST api on `127.0.01:3000`