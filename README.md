# fastapi-gino-uvicorn

This is a dockerized project template for building awesome restapis making use of FastApi, Gino and Uvicorn.

### Installation

Clone the repository and install poetry dependencies

```sh
$ git clone https://github.com/Gcunhaa/fastapi-gino-uvicorn.git
$ poetry install
```

### Run
Update develop-demo.env file then run docker compose:

```sh
$ sudo docker-compose -f setup/docker/docker-compose.dev.yml up --build
```

### Alembic migrations
You should edit the default settings for the PGSQL connection(core.settings.py) for some trash PGSQL server so you could do the migrations.

To prepare the migration:
```sh
poetry shell
PYTHONPATH=src alembic revision --autogenerate -m 'First migration'
```
Then the migration will be auto executed in the next docker startup.
### Todos

 - Make commands
 - Change migration actual style
 - Add production configs
