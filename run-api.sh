#!/bin/sh

cd api
gunicorn api:app
