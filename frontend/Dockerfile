FROM mhart/alpine-node:12

# install dependencies
WORKDIR /app
COPY src/package.json src/package-lock.json ./
RUN npm install
COPY src/ .
RUN npm run build

FROM caddy:2.1.1-alpine

COPY Caddyfile /etc/caddy/Caddyfile
COPY --from=0 /app/public /frontend
WORKDIR /frontend
