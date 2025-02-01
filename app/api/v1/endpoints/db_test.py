from fastapi import APIRouter
from db.mongodb import users_collection, uploads_collection
from schemas.user import UserUpdate
from bson import ObjectId

router = APIRouter()

@router.get("/users", tags=["DB"])
def get_all_users():
    """
    전체 사용자 데이터 조회 API
    """
    users = list(users_collection.find({}, {"_id": 1, "nickname": 1, "age": 1, "birthdate": 1}))
    
    # ObjectId를 문자열로 변환
    for user in users:
        user["_id"] = str(user["_id"])

    return {"users": users}

@router.get("/uploads", tags=["DB"])
def get_all_uploads():
    """
    업로드된 이미지 리스트 조회 API
    """
    uploads = list(uploads_collection.find({}, {"_id": 1, "filename": 1, "url": 1}))
    
    # ObjectId를 문자열로 변환
    for upload in uploads:
        upload["_id"] = str(upload["_id"])

    return {"uploads": uploads}

@router.patch("/user/{nickname}", tags=["DB"])
def update_user(nickname: str, user_update: UserUpdate):
    """
    특정 사용자의 나이 또는 생년월일을 업데이트하는 API
    """
    user = users_collection.find_one({"nickname": nickname})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = {}
    if user_update.age is not None:
        update_data["age"] = user_update.age
    if user_update.birthdate is not None:
        update_data["birthdate"] = str(user_update.birthdate)

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    users_collection.update_one({"nickname": nickname}, {"$set": update_data})
    return {"message": "User updated successfully", "updated_data": update_data}

@router.delete("/user/{nickname}", tags=["DB"])
def delete_user(nickname: str):
    """
    특정 사용자를 삭제하는 API
    """
    result = users_collection.delete_one({"nickname": nickname})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully", "nickname": nickname}