FROM nginx
COPY web /usr/share/nginx/html
COPY enermaps.conf /etc/nginx/conf.d/enermaps.conf
RUN mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.backup