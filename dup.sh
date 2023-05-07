#!/bin/bash

if [[ -z "$MYSQL_USER" ]]; then
  echo "Environment variable MYSQL_USER required!"
  exit 1
fi

if [[ -z "$MYSQL_PASSWORD" ]]; then
  echo "Environment variable MYSQL_PASSWORD required!"
  exit 1
fi

docker compose up --build --abort-on-container-exit
