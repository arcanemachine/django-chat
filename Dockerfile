# syntax=docker/dockerfile

FROM python:3.9-slim

# set python environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies
COPY ./app/requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache-dir -r /tmp/requirements.txt \
  && rm -rf /tmp/requirements.txt

# copy files
COPY --chown=1001:1001 ./app /app
COPY --chown=1001:1001 ./docker /docker
RUN chmod +x /docker/*.sh

USER 1001:1001
WORKDIR /app

ENTRYPOINT [ "/docker/entrypoint.sh" ]
CMD [ "/docker/start.sh", "server" ]
