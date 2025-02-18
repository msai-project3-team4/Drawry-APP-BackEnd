from fastapi import FastAPI
import os
from db.mongodb import db, collection
from api.v1.routers import api_router
from core.config import config


app = FastAPI()
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message: FastAPI 서버 실행 중"}
