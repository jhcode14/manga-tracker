#!/bin/sh

# cleanup after docker-compose up --build
# WARNING: this deletes all un-used docker images/containers/volumes

# Step 1: stop docker containers
docker-compose down

sleep 3

# Step 2: clean up
#docker system prune -f
#docker volume prune -f
docker rmi $(docker images 'tamago-*' -q)