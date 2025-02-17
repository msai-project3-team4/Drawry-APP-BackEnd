from fastapi import FastAPI
import os
from db.mongodb import db, collection
from db.redis_db import redis_client
from api.v1.routers import api_router



app = FastAPI()
app.include_router(api_router)

@app.get("/")
def read_root():

    return {"message": "좋은 예시건 나쁜 예시건 그런건 없어요 .. 두현님 명언제조기 .. "}
