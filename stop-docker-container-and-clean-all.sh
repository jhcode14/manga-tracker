#!/bin/sh

# cleanup after docker-compose up --build
# WARNING: this deletes all un-used docker images/containers/volumes

# Step 1: stop docker containers
docker-compose down

sleep 3

# Step 2: clean up
docker system prune -f
docker volume prune -f

# Function to remove image if it exists
remove_image_if_exists() {
    if docker image inspect "$1" >/dev/null 2>&1; then
        echo "Removing image: $1"
        docker rmi "$1"
    else
        echo "Image not found: $1"
    fi
}

# Remove specific images
remove_image_if_exists "manga-tracker-frontend:latest"
remove_image_if_exists "manga-tracker-backend:latest"