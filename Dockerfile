# syntax=docker/dockerfile

FROM python:3.9-slim-bullseye

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies
COPY ./app/requirements.txt .
RUN python3 -m pip install -r requirements.txt

# copy nginx config
# ARG server_environment=${SERVER_ENVIRONMENT}
# ARG project_name=${PROJECT_NAME}
# ADD ./nginx/${server_environment} /etc/nginx/

# copy django project
COPY ./app .
