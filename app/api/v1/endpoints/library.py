from fastapi import APIRouter, HTTPException
from db.mongodb import library_collection
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

router = APIRouter()

class LibraryCreate(BaseModel):
    nickname: str  # ✅ 닉네임을 기반으로 저장

class Book(BaseModel):
    id: Optional[str] = None
    title: str
    characters: List[str] = []  # ✅ 캐릭터 정보 추가

class LibraryResponse(BaseModel):
    nickname: str
    books: List[Book] = []

class AddCharacter(BaseModel):
    character: str

# ✅ (1) 특정 사용자의 서재 조회
@router.get("/library/{nickname}", response_model=LibraryResponse)
def get_library(nickname: str):
    library = library_collection.find_one({"nickname": nickname})
    if library:
        books = [Book(**book) for book in library.get("books", [])]
        return LibraryResponse(nickname=nickname, books=books)
    else:
        raise HTTPException(status_code=404, detail="서재가 비어 있습니다.")

# ✅ (2) 서재 생성
@router.post("/library")
def create_library(library_data: LibraryCreate):
    existing_library = library_collection.find_one({"nickname": library_data.nickname})
    if existing_library:
        raise HTTPException(status_code=400, detail="이미 서재가 존재합니다.")
    
    new_library = {"nickname": library_data.nickname, "books": []}
    library_collection.insert_one(new_library)
    return {"message": "서재가 생성되었습니다."}

# ✅ (3) 서재 삭제
@router.delete("/library/{nickname}")
def delete_library(nickname: str):
    result = library_collection.delete_one({"nickname": nickname})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="서재를 찾을 수 없습니다.")
    return {"message": "서재가 삭제되었습니다."}

# ✅ (4) 서재에 동화책 추가 (저자 제거, 캐릭터 리스트 추가)
@router.post("/library/{nickname}/books", response_model=Book)
def add_book(nickname: str, book: Book):
    library = library_collection.find_one({"nickname": nickname})
    if not library:
        raise HTTPException(status_code=404, detail="서재를 찾을 수 없습니다.")
    
    new_book = {"id": str(ObjectId()), "title": book.title, "characters": book.characters}
    library_collection.update_one({"nickname": nickname}, {"$push": {"books": new_book}})
    
    return Book(**new_book)

# ✅ (5) 서재의 특정 동화책에 캐릭터 추가
@router.patch("/library/{nickname}/books/{book_id}/characters")
def add_character(nickname: str, book_id: str, character_data: AddCharacter):
    library = library_collection.find_one({"nickname": nickname})
    if not library:
        raise HTTPException(status_code=404, detail="서재를 찾을 수 없습니다.")

    book_index = next((i for i, book in enumerate(library.get("books", [])) if book["id"] == book_id), None)
    if book_index is None:
        raise HTTPException(status_code=404, detail="책을 찾을 수 없습니다.")

    updated_books = library["books"]
    updated_books[book_index]["characters"].append(character_data.character)

    library_collection.update_one({"nickname": nickname}, {"$set": {"books": updated_books}})
    return {"message": "캐릭터가 추가되었습니다.", "characters": updated_books[book_index]["characters"]}
