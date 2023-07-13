# Start application
```
cd app

uvicorn main:app --reload 
```

# Start Docker

```
docker run -p 8000:8000 intership-be
```
# Make migrations
```
alembic revision --autogenerate -m "migration_name"
```
## Upgrade migrations
```
alembic upgrade head
```