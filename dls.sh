#!/bin/bash

echo "----- Images -----"
sudo docker images -a
echo
echo "----- Containers -----"
sudo docker ps -a
echo
echo "----- Services -----"
sudo docker compose ps -a
echo