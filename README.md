# Fastapi app for spimex trade results

## Quickstart

- **run docker compose**
```
docker compose --env-file .env-compose.template up -d
```

- **run fastapi**
```
uvicorn app.main:app --reload
```

- **run tests**
```
pytest
```

- **run tests with coverage**
```
pytest --cov
```


## Configuration

- **example of .env file for docker compose**
```
# env variables using by docker compose yml file

# main-db
DB_USER=wm-user
DB_PASSWORD=wm-password
DB_NAME=wm-db-name

# test-db
TEST_DB_USER=wm-user-test
TEST_DB_PASSWORD=wm-password-test
TEST_DB_NAME=wm-db-name-test

```


- **example of .env file for porject**
```
# config vairables that need to create to run application

# Run application
CONFIG__RUN__APP=main:app
CONFIG__RUN__HOST=0.0.0.0
CONFIG__RUN__PORT=8000
CONFIG__RUN__AUTO_RELOAD=True

# Main database
CONFIG__MAIN_PG_DB__DB_USER=wm-user
CONFIG__MAIN_PG_DB__DB_PASSWORD=wm-password
CONFIG__MAIN_PG_DB__DB_HOST=localhost
CONFIG__MAIN_PG_DB__DB_PORT=5431
CONFIG__MAIN_PG_DB__DB_NAME=wm-db-name

# Test database
CONFIG__TEST_PG_DB__DB_USER=wm-user-test 
CONFIG__TEST_PG_DB__DB_PASSWORD=wm-password-test
CONFIG__TEST_PG_DB__DB_HOST=localhost
CONFIG__TEST_PG_DB__DB_PORT=5430
CONFIG__TEST_PG_DB__DB_NAME=wm-db-name-test

# Redis cache
CONFIG__REDIS_CACHE__REDIS_HOST=localhost
CONFIG__REDIS_CACHE__REDIS_PORT=6380
CONFIG__REDIS_CACHE__REDIS_DB=0
```