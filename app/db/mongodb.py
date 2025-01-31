# MongoDB 연결이 실패하면 일정 시간 동안 재시도하는 로직을 추가

from pymongo import MongoClient
import time
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/mydatabase")

def get_mongo_client():
    max_retries = 5
    retry_delay = 2 # 2초 간격으로 재시도

    for i in range(max_retries):
        try:
            client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            client.admin.command("ping") # MongoDB 연결 확인
            print("✅ MongoDB 연결 성공")
            return client
        except Exception as e:
            print(f"⚠️ MongoDB 연결 실패 ({i+1}/{max_retries}) - {e}")
    
    raise Exception("❌ MongoDB 연결 실패: 최대 재시도 횟수를 초과함")

mongo_client = get_mongo_client()
db = mongo_client["mydatabase"]
collection = db["test_collection"]