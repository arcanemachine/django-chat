# django-chat

A basic chat app created using Django, Django Rest Framework, and a little bit of Vue.


## Instructions

- Install `docker` and `docker-compose`
- Run `1--secret-key-generate` to generate a new secret key.
- Run `2--server-config-choose` to select the environment type (dev, test, or prod).
  - e.g. `2--server-config-choose dev` to use a dev environment
- Start the container:
  - For development environments:
    - Run `docker-compose -f docker-compose.yml -f docker-compose.dev.yml up`
  - For test environments:
    - Run `docker-compose -f docker-compose.yml -f docker-compose.test.yml up`
  - For production environments:
    - Run `docker-compose -f docker-compose.yml -f docker-compose.prod.yml up`

## Environment Types

- dev:
  - Debug mode enabled
  - Uses built-in Django server `runserver` to serve all content
- test: Same as prod
- prod:
  - Debug mode disabled
  - Uses gunicorn to serve Django content
  - Uses nginx container to serve static/media content
