# 회원가입 API
from fastapi import APIRouter, HTTPException
from db.mongodb import db
from schemas.user import UserCreate, UserLogin, UserUpdate
from core.security import create_access_token

from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
users_collection = db["users"]
#닉네임을 `unique`로 설정하여 중복 방지
users_collection.create_index("nickname", unique=True)



# 일반 사용자 API
@router.post("/register")
def register(user: UserCreate):
    # ✅ 닉네임이 None이거나 빈 문자열이면 예외 처리
    if not user.nickname or user.nickname.strip() == "":
        raise HTTPException(status_code=400, detail="닉네임은 필수 입력값입니다.")

    # ✅ 닉네임 중복 검사
    if users_collection.find_one({"nickname": user.nickname}):
        raise HTTPException(status_code=400, detail="이미 존재하는 닉네임입니다.")

    # ✅ 사용자 저장
    user_data = {
        "nickname": user.nickname.strip(),  # ✅ 공백 제거 후 저장
        "age": user.age,
        "birthdate": str(user.birthdate),
    }
    users_collection.insert_one(user_data)

    return {"message": "회원가입이 완료되었습니다.", "nickname": user.nickname}


#  (2) 로그인 API
@router.post("/login")
def login(user: UserLogin):
    # 사용자 조회
    existing_user = users_collection.find_one({"nickname": user.nickname})
    if not existing_user:
        raise HTTPException(status_code=400, detail="사용자를 찾을 수 없습니다.")

    # JWT 토큰 발급
    access_token = create_access_token(data={"sub": existing_user["nickname"]}, expires_delta=timedelta(hours=1))
    return {"access_token": access_token, "token_type": "bearer"}

#  (3) 사용자 정보 수정 API
@router.patch("/users/{nickname}")
def update_user(nickname: str, user_update: UserUpdate):
    existing_user = users_collection.find_one({"nickname": nickname})
    if not existing_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    update_data = {}
    if user_update.age is not None:
        update_data["age"] = user_update.age
    if user_update.birthdate is not None:
        update_data["birthdate"] = str(user_update.birthdate)

    users_collection.update_one({"nickname": nickname}, {"$set": update_data})
    return {"message": "사용자 정보가 업데이트되었습니다."}