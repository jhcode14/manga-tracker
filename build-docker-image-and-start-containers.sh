#!/bin/sh

# Step 1: build docker image
docker build -t manga-tracker-backend .
docker build -f frontend/Dockerfile -t manga-tracker-frontend .

# Step 2: run docker compose in detached mode
docker-compose up -d --build