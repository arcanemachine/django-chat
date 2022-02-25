# syntax=docker/dockerfile

FROM python:3.9-slim-bullseye

# set python environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# work in /code
WORKDIR /code

# copy code to container
COPY ./src /code
RUN pip install -r requirements.txt
