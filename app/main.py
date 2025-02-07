from fastapi import FastAPI
import os
from db.mongodb import db, collection
from db.redis_db import redis_client
from api.v1.routers import api_router



app = FastAPI()
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "PR 두번째 시도"}
    return {"message": "Welcome to the HelloWorld"}

