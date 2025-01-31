import redis
import time
import os

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

def get_redis_client():
    max_retries = 5
    retry_delay = 2

    for i in range(max_retries):
        try:
            client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
            client.ping()  # Redis 연결 확인
            print("✅ Redis 연결 성공")
            return client
        except Exception as e:
            print(f"⚠️ Redis 연결 실패 ({i+1}/{max_retries}) - {e}")
            time.sleep(retry_delay)

    raise Exception("❌ Redis 연결 실패: 최대 재시도 횟수를 초과함")

redis_client = get_redis_client()
