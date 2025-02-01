from fastapi import APIRouter, UploadFile, File, HTTPException
import os
from datetime import datetime

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", tags=["Upload"])
async def upload_image(file: UploadFile = File(...)):
    """
    사용자가 업로드한 스케치 이미지를 저장하는 API
    """
    allowed_extensions = {"png", "jpg", "jpeg"}
    extension = file.filename.split(".")[-1].lower()
    if extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Only PNG, JPG, JPEG files are allowed")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return {"filename": filename, "url": f"/uploads/{filename}", "message": "Upload successful"}
