#!/bin/sh

# Step 1: build docker image
docker build -t manga-tracker-backend .

# Step 2: run docker compose
docker-compose up