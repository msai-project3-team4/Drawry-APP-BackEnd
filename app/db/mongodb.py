import time
import logging
from pymongo import MongoClient
from core.config import config  # ✅ 환경 변수 가져오기

# ✅ 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDB:
    """MongoDB 연결 및 관리"""

    @staticmethod
    def get_mongo_client():
        """MongoDB 연결을 시도하고 실패 시 재시도하는 함수"""
        max_retries = 5
        retry_delay = 2  # 2초 간격으로 재시도

        for i in range(max_retries):
            try:
                client = MongoClient(config.MONGO_URI, serverSelectionTimeoutMS=5000)
                client.admin.command("ping")  # MongoDB 연결 확인
                logger.info("✅ MongoDB 연결 성공")
                return client
            except Exception as e:
                logger.warning(f"⚠️ MongoDB 연결 실패 ({i+1}/{max_retries}) - {e}")
                time.sleep(retry_delay)  # 재시도 전 대기
        
        logger.error("❌ MongoDB 연결 실패: 최대 재시도 횟수를 초과함")
        raise Exception("MongoDB 연결 실패")

# ✅ 전역 MongoDB 클라이언트 생성
mongo_client = MongoDB.get_mongo_client()
db = mongo_client["mydatabase"]

# ✅ 컬렉션 정의 (다른 모듈에서 쉽게 사용 가능)
collection = db["test_collection"]
users_collection = db["users"]
users_collection.create_index("nickname", unique=True)

uploads_collection = db["uploads"]
library_collection = db["library"]
