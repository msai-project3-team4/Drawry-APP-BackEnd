from fastapi import APIRouter, HTTPException
from db.mongodb import users_collection
from models.user import User

router = APIRouter()

# ✅ (1) 사용자 등록
@router.post("/users")
def create_user(user: User):
    existing_user = users_collection.find_one({"user_id": user.user_id})
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 닉네임입니다.")

    users_collection.insert_one(user.dict())
    return {"message": "사용자가 등록되었습니다.", "user": user}

# ✅ (2) 사용자 조회
@router.get("/users/{user_id}")
def get_user(user_id: str):
    user = users_collection.find_one({"user_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    return {"user_id": user["user_id"], "nickname": user["nickname"], "age": user["age"], "birthdate": user["birthdate"]}
