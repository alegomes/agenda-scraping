#!/bin/bash

echo "----- Stopping services -----"
./ddw.sh
echo
echo "----- Removing containers -----"
sudo docker rm --force $(sudo docker ps -aq)
echo
echo "----- Removing images  -----"
sudo docker image rm --force $(sudo docker images -aq)
echo
echo "----- Removing services -----"
sudo docker compose rm $(sudo docker compose ps -aq)
echo
./dls.sh
echo