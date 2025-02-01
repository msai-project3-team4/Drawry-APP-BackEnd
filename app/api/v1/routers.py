from fastapi import APIRouter
from api.v1.endpoints import auth, upload, db_test

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["인증"])
api_router.include_router(db_test.router, prefix="/db", tags=["DB"])
api_router.include_router(upload.router, prefix="/upload", tags=["Upload"])