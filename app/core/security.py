from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.config import config

# JWT 토큰 발급을 위한 OAuth2 설정
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)):
    """
    JWT 액세스 토큰 생성 함수
    :param data: 토큰에 포함할 데이터 (예: {"sub": "nickname"})
    :param expires_delta: 토큰 만료 시간 (기본값: 60분)
    :return: JWT 액세스 토큰 (str)
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})  # 만료 시간 추가
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)

def verify_access_token(token: str = Depends(oauth2_scheme)):
    """
    JWT 토큰 검증 함수
    :param token: 클라이언트가 보낸 JWT 토큰
    :return: 유효한 경우 닉네임 반환, 유효하지 않으면 401 에러 발생
    """
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        nickname: str = payload.get("sub")
        if nickname is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return nickname
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )