# 회원가입 API
from fastapi import APIRouter, HTTPException
from db.mongodb import db
from schemas.user import UserCreate
from core.security import create_access_token
from schemas.user import UserLogin
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

KAKAO_CLIENT_ID = os.getenv("KAKAO_CLIENT_ID")
KAKAO_REDIRECT_URI = os.getenv("KAKAO_REDIRECT_URI")

# 카카오 로그인 API
@router.post("/auth/kakao")
def kakao_login(access_token: str):
    """카카오 로그인 후 사용자 정보를 백엔드로 전달"""

    # ✅ 카카오 API에서 사용자 정보 가져오기
    headers = {"Authorization": f"Bearer {access_token}"}
    kakao_user_url = "https://kapi.kakao.com/v2/user/me"

    response = requests.get(kakao_user_url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="카카오 사용자 정보 요청 실패")

    kakao_user = response.json()

    # ✅ 카카오에서 받은 정보
    nickname = kakao_user.get("properties", {}).get("nickname", "사용자")
    email = kakao_user.get("kakao_account", {}).get("email", None)

    if not email:
        raise HTTPException(status_code=400, detail="이메일 정보가 필요합니다.")

    users_collection = db["users"]

    # ✅ 기존 사용자 확인
    existing_user = users_collection.find_one({"email": email})
    if not existing_user:
        # 신규 사용자 회원가입
        user_data = {
            "nickname": nickname,
            "email": email,
            "age": None,
            "birthdate": None,
        }
        users_collection.insert_one(user_data)
        existing_user = user_data

    # ✅ JWT 토큰 발급
    access_token = create_access_token(data={"sub": existing_user["email"]}, expires_delta=timedelta(hours=1))

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "nickname": existing_user["nickname"],
        "email": existing_user["email"]
    }

# 일반 사용자 API
@router.post("/register")
def register(user: UserCreate):
    users_collection = db["users"]

    # 닉네임 중복 검사
    if users_collection.find_one({"nickname": user.nickname}):
        raise HTTPException(status_code=400, detail="Nickname already taken")
    
    # 사용자 저장
    user_data = {
        "nickname": user.nickname,
        "age": user.age,
        "birthdate": str(user.birthdate),
    }
    users_collection.insert_one(user_data)

    return {"message": "User registered successfully", "nickname": user.nickname}


@router.post("/login")
def login(user: UserLogin):
    users_collection = db["users"]

    # 사용자 조회
    existing_user = users_collection.find_one({"nickname": user.nickname})
    if not existing_user:
        raise HTTPException(status_code=400, detail="User not found")


    # JWT 토큰 발급
    access_token = create_access_token(data={"sub": existing_user["nickname"]}, expires_delta= timedelta(hours=1))
    return {"access_token": access_token, "token_type": "bearer"}