#!/bin/bash

cd /app

if [ $# -eq 0 ]; then
    echo "Usage: start.sh [PROCESS_TYPE](server/beat/worker/flower)"
    exit 1
fi

PROCESS_TYPE=$1

if [ "$PROCESS_TYPE" = "server" ]; then
  if [ "$SERVER_ENVIRONMENT" = "dev" ]; then
    exec python3 manage.py runserver 0.0.0.0:$PROJECT_PORT_INTERNAL
  elif [ "$SERVER_ENVIRONMENT" = "test" ] || [ "$SERVER_ENVIRONMENT" = "prod" ]; then
    exec gunicorn \
      --bind 0.0.0.0:8000 \
      --workers 1 \
      --worker-class eventlet \
      --log-level DEBUG \
      --access-logfile "-" \
      --error-logfile "-" \
      $PROJECT_NAME_PYTHON.wsgi
  fi
elif [ "$PROCESS_TYPE" = "beat" ]; then
  celery \
    --app dockerapp.celery_app \
    beat \
    --loglevel INFO \
    --scheduler django_celery_beat.schedulers:DatabaseScheduler
elif [ "$PROCESS_TYPE" = "flower" ]; then
  celery \
    --app dockerapp.celery_app \
    flower \
    --basic_auth="${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}" \
    --loglevel INFO
elif [ "$PROCESS_TYPE" = "worker" ]; then
  celery \
    --app dockerapp.celery_app \
    worker \
    --loglevel INFO
fi
