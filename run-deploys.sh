#!/bin/sh

if test "$DEPLOY" = 'api'
then
	cd api
	python3 api.py --port $PORT
elif test "$DEPLOY" = 'app'
then
	cd client
	python3 main.py --port $PORT
else
	cat >&2 <<'eof'
Server environment is not configured
Run `heroku config:set DEPLOY=api --remote heroku-api'
Run `heroku config:set DEPLOY=app --remote heroku-app'
eof
	exit 1
fi
