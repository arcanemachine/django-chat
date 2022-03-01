# django-chat

A basic chat app created using Django, Django Rest Framework, and a little bit of Vue.


## Instructions

- Install `docker` and `docker-compose`
- Start the container:
  - For development environments:
    - Optional: Use Traefik as a reverse-proxy:
      - Run `docker-compose -f docker-compose.traefik.yml up` (Access dashboard from `http://monitor.localhost/`)
    - Run `docker-compose -f docker-compose.yml -f docker-compose.dev.yml up` (Access server from `localhost:8004`)
      - If Traefik is running, the server can be accessed from `http://django-chat.localhost`.
  - These next sections are for personal use only. You will need to setup Traefik with some slight modifications (e.g. remove the middleware config):
    - For test environments:
      - Run `docker-compose -f docker-compose.yml -f docker-compose.test.yml up`
      - Must be deployed with Traefik or a modified nginx config
    - For production environments:
      - Run `docker-compose -f docker-compose.yml -f docker-compose.prod.yml up`
      - Must be deployed with Traefik or a modified nginx config

## Environment Types

- dev:
  - Debug mode enabled
  - Uses built-in Django server `runserver` to serve all content
- test: Same as prod
- prod:
  - Debug mode disabled
  - Uses gunicorn to serve Django content
  - Uses nginx container to serve static/media content
