# Manga Tracker

Hey! Thanks for stopping by. This is a full-stack app that I built to track my manga reading progress.

The app is built with React and Node.js (Frontend) and Python Flask+PostgreSQL (Backend). The application is containerized and indended to be hosted on-prim.

This is what the it looks like:

<img src="./manga-shelf.gif" alt="drawing" width="300"/>

Check it out on: http://localhost:5173/ (Just kidding LOL)

## Setup

### Virtual Enviornment

This project libaries is maintained by venv, to get started:

0. Setup venv for the first time
   Create a virtual environment named 'myenv'
   `python3 -m venv myenv`

`source myenv/bin/activate`

1. Run to start virtual-env:
   `source .venv/bin/activate`

### Install Python v3.10:

- pyenv
  -- Install new python version (and use it)
  `pyenv install 3.10 && pyenv global 3.10`

### Run application

#### Option 1: Run With Scripts

`./stop-docker-container-and-clean-all.sh && ./build-docker-image-and-start-containers.sh`

#### Option 2: Run With Individual Docker Commands

##### Build docker image, start db and web app:

`docker-compose up --build`

`docker-compose up -d # Recreate and start containers in detached mode`

##### Interact with PostgreSQL in db container

`docker exec -it mt_postgres_container psql -U user -d mydatabase`

##### Stop and remove containers

`docker-compose down`

##### Clean up (WARNING: This deletes all volumes, images, and containers)

`docker volume prune`
`docker system prune`
or
`docker image prune`
`docker container prune`

##### Remove individually

`docker volume rm <volume_name>`
