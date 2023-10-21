# Start application
```
cd app

uvicorn main:app --reload 

or

uvicorn app.main:app  --host 0.0.0.0 --port 8080 --no-use-colors

```

# Start Docker (useless)
```
docker run -p 8000:8000 intership-be
```
# Start Docker-compose (up databases)
```
docker-compose up -d
```

# Make migrations
```
alembic revision --autogenerate -m "migration_name"
```
## Upgrade migrations
```
alembic upgrade head
```