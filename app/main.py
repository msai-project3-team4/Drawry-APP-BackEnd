from fastapi import FastAPI
from pymongo import MongoClient
import redis
import os
from db.mongodb import db, collection
from db.redis_db import redis_client
from bson import ObjectId  # ObjectId 변환



app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "안녕하세요 1월 31일 GIT 테스트., FastAPI Backend with MongoDB & Redis!"}

@app.get("/mongo-test")
def mongo_test():
    doc = {"name": "Test User", "age": 25}
    result = collection.insert_one(doc)  # MongoDB에 삽입
    inserted_id = str(result.inserted_id)  # ObjectId를 문자열로 변환
     # 삽입한 데이터 조회 후 `_id` 변환
    inserted_doc = collection.find_one({"_id": result.inserted_id})
    inserted_doc["_id"] = str(inserted_doc["_id"])  # `_id`를 JSON 직렬화 가능하도록 변환

    return {
        "message": "Inserted into MongoDB!",
        "inserted_id": inserted_id,
        "data": inserted_doc
    }

@app.get("/mongo-fetch")
def fetch_mongo():
    data = collection.find_one({"name": "Test User"})  # 데이터 조회
    if data:
        data["_id"] = str(data["_id"])  # ObjectId를 문자열로 변환
        return {
            "message": "Fetched from MongoDB!",
            "data": data
        }
    return {"message": "No data found!"}

@app.get("/redis-test")
def redis_test():
    redis_client.set("test_key", "Hello Redis!")
    value = redis_client.get("test_key")
    return {"message": "Value from Redis", "data": value}
