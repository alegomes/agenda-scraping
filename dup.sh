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

sudo docker compose up --build --abort-on-container-exit
