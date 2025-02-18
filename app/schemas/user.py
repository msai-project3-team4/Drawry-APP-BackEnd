from pydantic import BaseModel
from datetime import date
from typing import Optional

# ✅ 회원가입 요청 스키마
class UserCreate(BaseModel):
    nickname: str  # ✅ 닉네임을 고유한 ID로 사용
    age: int
    birthdate: date

# ✅ 로그인 요청 스키마
class UserLogin(BaseModel):
    nickname: str  # ✅ 로그인 시 닉네임을 nickname로 사용

# ✅ 사용자 정보 업데이트 스키마
class UserUpdate(BaseModel):
    age: Optional[int] = None
    birthdate: Optional[date] = None
