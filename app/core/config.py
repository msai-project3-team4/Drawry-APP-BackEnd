import os
import time
import redis
from dotenv import load_dotenv

class Config:
    """환경 변수 및 Redis 설정 클래스"""

    # ✅ 환경 변수 로드 (클래스가 처음 호출될 때 실행)
    @classmethod
    def load_env(cls):
        load_dotenv()
        cls.SECRET_KEY = os.getenv("SECRET_KEY")
        cls.MONGO_URI = os.getenv("MONGO_URI")
        cls.REDIS_HOST = os.getenv("REDIS_HOST")
        cls.REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
        
        cls.ALGORITHM = os.getenv("ALGORITHM", "HS256")
        cls.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))  # ✅ 기본값 설정 필요



    # ✅ Redis 연결 (전역 객체)
    @classmethod
    def get_redis_client(cls):
        max_retries = 5
        retry_delay = 2

        for i in range(max_retries):
            try:
                client = redis.Redis(host=cls.REDIS_HOST, port=cls.REDIS_PORT, decode_responses=True)
                client.ping()  # Redis 연결 확인
                print("✅ Redis 연결 성공")
                return client
            except Exception as e:
                print(f"⚠️ Redis 연결 실패 ({i+1}/{max_retries}) - {e}")
                time.sleep(retry_delay)

        raise Exception("❌ Redis 연결 실패: 최대 재시도 횟수를 초과함")

# ✅ 환경 변수 로드 실행
Config.load_env()

# ✅ Redis 클라이언트 인스턴스 생성
redis_client = Config.get_redis_client()

# ✅ 환경 변수 설정 인스턴스 생성
config = Config()
