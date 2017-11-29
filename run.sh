#!/bin/sh
cat config/nginx.conf.template | sed s#{STATIC_FILES_URL}#$STATIC_FILES_URL#g > /etc/nginx/conf.d/default.conf

mkdir -p /run/nginx
nginx
#uwsgi --ini config/uwsgi.trove.ini &
uwsgi --ini config/uwsgi.risse.ini