# Start application
```
cd app

uvicorn main:app --reload 
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