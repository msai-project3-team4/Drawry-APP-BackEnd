# 회원가입 요청 스키마
from pydantic import BaseModel
from datetime import date
from typing import Optional

class UserCreate(BaseModel):
    nickname: str
    age: int
    birthdate: date

class UserLogin(BaseModel):
    nickname: str


class UserUpdate(BaseModel):
    age: Optional[int] = None
    birthdate: Optional[date] = None