#!/bin/sh
set -eu

envsubst < /usr/share/nginx/html/env-config.template.js > /usr/share/nginx/html/env-config.js
