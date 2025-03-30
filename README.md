# Tamago

Hey! Thanks for stopping by. This is a full-stack app that I built to track my manga reading progress.

The app is built with React and Node.js (Frontend) and Python Flask+PostgreSQL (Backend). The application is containerized and indended to be hosted on-prim.

This is what the it looks like:

<img src="./manga-shelf.gif" alt="drawing" width="300"/>

Check it out on: http://localhost:5173/ (Just kidding - look below for how to run it yourself)

## Setup

### Virtual Enviornment

This project libaries is maintained by venv, to get started:

0. Setup venv for the first time
   Create a virtual environment named 'myenv'
   `python3 -m venv myenv`

`source myenv/bin/activate`

1. Run to start virtual-env:
   `source .venv/bin/activate`

2. (Optional) If developing, install all the required dependencies
   `pip install -r app/requreiemnts.txt`

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

### Database Migreation

Backup existing database:
`docker exec -i mt_postgres_container pg_dump -U user mydatabase > backup.sql`

Add new migration script to migratino folder, Pipe the SQL directly into psql in container, for example:
`cat config/migrations/001_add_last_updated.sql | docker exec -i mt_postgres_container psql -U user -d mydatabase`

Double check schema changes successfully, for example:
`docker exec -it mt_postgres_container psql -U user -d mydatabase`
`SELECT * FROM information_schema.columns WHERE table_name='manga' AND column_name='last_updated';`
