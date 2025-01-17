This project libaries is maintained by venv, to get started:

# Virtual Enviornment

0. Setup venv for the first time
   Create a virtual environment named 'myenv'
   `python3 -m venv myenv`

`source myenv/bin/activate`

1. Run to start virtual-env:
   `source .venv/bin/activate`

# Install Python v3.10:

- pyenv
  -- Install new python version (and use it)
  `pyenv install 3.10 && pyenv global 3.10`

# Run application

## Option 1: Run With Scripts

`./stop-docker-container-and-clean-all.sh && ./build-docker-image-and-start-containers.sh`

## Option 2: Run With Individual Docker Commands

### Build docker image, start db and web app:

`docker-compose up --build`

`docker-compose up -d # Recreate and start containers in detached mode`

### Interact with PostgreSQL in db container

`docker exec -it mt_postgres_container psql -U user -d mydatabase`

### Stop and remove containers

`docker-compose down`

### Clean up

#### (WARNING: This deletes all)

`docker volume prune`
`docker system prune`
or
`docker image prune`
`docker container prune`

#### Remove individually

`docker volume rm <volume_name>`
