from fastapi import FastAPI
from .db.db import engine, r

app = FastAPI()

@app.on_event("startup")
async def startup():
    await engine.connect()

# @app.on_event("shutdown")
# async def shutdown():
#     await engine.dispose()

@app.get("/")
def health_check():
    return {
        "status_code": 200,
        "detail": "ok",
        "result": "working"
    }
