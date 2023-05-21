#!/bin/bash

if [[ ! -f .env ]]; then
  echo
  echo "---> .env file not found <---"
  echo
  echo "Create it with both MYSQL_USER and MYSQL_PASSWORD inside."
  echo "  echo MYSQL_USER=youruser >> .env"
  echo "  echo MYSQL_PASSWORD=yourpassword >> .env"
  echo
  exit 1

fi

#if [[ -z "$MYSQL_USER" ]]; then
#  echo "Environment variable MYSQL_USER required!"
#  echo "Add it to a .env file and run $0 again"
#  echo
#  echo "  echo MYSQL_USER=youruser >> .env"
#  exit 1
#fi

#if [[ -z "$MYSQL_PASSWORD" ]]; then
#  echo "Environment variable MYSQL_PASSWORD required!"
#  exit 1
#fi

sudo docker compose up --build --abort-on-container-exit