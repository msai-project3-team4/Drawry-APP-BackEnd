# 회원정보를 저장하는 모델
from pydantic import BaseModel, Field
from datetime import date
from bson import ObjectId

class User(BaseModel):
    nickname: str # 닉네임
    age: int # 나이
    birthdate: date # 생년월일

    class Config:
        orm_mode = True