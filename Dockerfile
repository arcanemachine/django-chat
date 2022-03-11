# syntax=docker/dockerfile

FROM docker.io/python:3.9-slim as base

# set args
ARG app_home=/app
ARG app_user=app-user

# set python environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# create and switch to user
RUN useradd --system --user-group --create-home $app_user

# switch to non-root user and do time-intensive stuff before switching back to root
USER $app_user

# add local python packages to PATH
ENV PATH=/home/${USERNAME}/.local/bin:$PATH

# install dependencies
COPY ./app/requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --upgrade pip --no-cache-dir --no-warn-script-location \
  && python3 -m pip install -r /tmp/requirements.txt --no-cache-dir --no-warn-script-location

# switch back to root
USER root
RUN rm /tmp/requirements.txt

# copy files and set permissions
COPY --chown=$app_user:$app_user ./app /app
COPY --chown=$app_user:$app_user ./docker /docker
RUN chmod +x /docker/*.sh
CMD [ "sleep", "1000" ]

USER $app_user
WORKDIR $app_home
VOLUME /app
ENTRYPOINT [ "/docker/entrypoint.sh" ]
CMD [ "/docker/start.sh", "server" ]
