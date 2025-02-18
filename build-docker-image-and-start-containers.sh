#!/bin/sh

# Step 1: build docker image
docker build -t manga-tracker-backend .
docker build -f frontend/Dockerfile -t manga-tracker-frontend .

# Step 2: run docker compose
docker-compose up