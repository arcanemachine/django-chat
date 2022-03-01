# django-chat

A basic chat app created using Django, Django Rest Framework, and a little bit of Vue.


## Instructions

- Install `docker` and `docker-compose`
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
