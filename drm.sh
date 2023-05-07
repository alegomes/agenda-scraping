#!/bin/bash

docker rm --force $(docker ps -aq)
docker image rm --force $(docker images -aq)
