# Fastapi app for spimex trade results

- run docker compose
```
docker compose --env-file .env-compose.template up -d
```

- run fastapi
```
uvicorn app.main:app --reload
```
