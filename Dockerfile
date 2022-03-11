# syntax=docker/dockerfile

FROM docker.io/python:3.9-slim-bullseye

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies
COPY ./app/requirements.txt .
RUN python3 -m pip install -r requirements.txt --no-cache-dir 

ENTRYPOINT [ "/docker/entrypoint.sh" ]
CMD [ "/docker/start.sh", "server" ]
