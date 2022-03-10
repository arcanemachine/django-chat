#!/bin/bash

app_path=$(dirname "$0")
environment_config_file_path="$app_path/server_config.$SERVER_ENVIRONMENT.py"
django_config_file_path="$app_path/server_config.py"


if [ "$SERVER_ENVIRONMENT" == "" ]; then
  if [ "$1" != "" ]; then
    $SERVER_ENVIRONMENT=$1
  else
    echo "SERVER_ENVIRONMENT not set. Aborting..."
    exit 1
  fi
fi

if [ "$SERVER_ENVIRONMENT" != "dev" ] && [ "$SERVER_ENVIRONMENT" != "test" ] && [ "$SERVER_ENVIRONMENT" != "prod" ]; then
  echo "SERVER_ENVIRONMENT must be one of: dev, test, prod"
  exit 1
fi

cd $app_path

# ensure secret_key.py exists
secret_key_path="$app_path/secret_key.py"
if [ ! -f $secret_key_path ]; then
  echo "Generating new SECRET_KEY..."
  echo "SECRET_KEY = '$(openssl rand -base64 48)'" > $secret_key_path
else
  echo "SECRET_KEY already exists. Moving on..."
fi

# use proper server_config_file
echo "Using '$SERVER_ENVIRONMENT' settings for server config..."
cp $environment_config_file_path $django_config_file_path
