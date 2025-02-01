# 회원가입 API
from fastapi import APIRouter, HTTPException
from db.mongodb import db
from schemas.user import UserCreate
from core.security import create_access_token
from schemas.user import UserLogin
from datetime import timedelta

router = APIRouter()

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