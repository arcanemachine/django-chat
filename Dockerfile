# syntax=docker/dockerfile

FROM python:3.9-slim-bullseye

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# copy over files for the correct server environment (e.g. dev, test, prod)
# ADD ./${SERVER_ENVIRONMENT:-dev} /

# install dependencies
COPY ./app/requirements.txt .
RUN python3 -m pip install -r requirements.txt

# copy project to container
COPY ./app .
