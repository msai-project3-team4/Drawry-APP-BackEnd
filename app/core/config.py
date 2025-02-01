import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Config:
    """환경 변수 설정 클래스"""

    # MongoDB 설정
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/mydatabase")

    # JWT 설정
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")  # 기본값 설정 (보안상 추천하지 않음)
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))  # 기본값: 60분

config = Config()
