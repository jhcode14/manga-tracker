#!/bin/sh

# Step 1: build docker image
docker build -t manga-tracker-backend .
docker build -t manga-tracker-scheduler . # Using the same Dockerfile as backend
docker build -t manga-tracker-frontend ./frontend

# Step 2: run docker compose
docker-compose up