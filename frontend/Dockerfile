FROM mhart/alpine-node:12

# install dependencies
WORKDIR /app
COPY src/package.json src/package-lock.json ./
COPY src/ .
RUN npm run build

FROM caddy:2.1.1-alpine

COPY Caddyfile /etc/caddy/Caddyfile
COPY --from=0 /app/public /frontend
WORKDIR /frontend

#RUN caddy validate
# IMPORTANT: Don't use this Dockerfile in your own Sapper projects without also looking at the .dockerignore file.
# Without an appropriate .dockerignore, this Dockerfile will copy a large number of unneeded files into your image.

