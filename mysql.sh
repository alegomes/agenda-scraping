#!/bin/bash

docker exec -it $(docker ps | grep agenda-scraping-db | cut -d ' ' -f 1) mysql