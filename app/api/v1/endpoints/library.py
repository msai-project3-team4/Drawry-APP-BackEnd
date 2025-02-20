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
    is_empty: bool  # ✅ 서재가 비어 있는지 여부 확인

class AddCharacter(BaseModel):
    character: str

class UpdateBookTitle(BaseModel):
    new_title: str  # ✅ 책 제목 수정용

class StorySelction(BaseModel):
    story: str
    character: str

# ✅ (1) 특정 사용자의 서재 조회
@router.get("/library/{nickname}", response_model=LibraryResponse)
def get_library(nickname: str):
    library = library_collection.find_one({"nickname": nickname})

    if library:
        books = library.get("books", [])  # ✅ books 필드 기본값 설정
        return LibraryResponse(nickname=nickname, books=books, is_empty=len(books) == 0)
    else:
        return LibraryResponse(nickname=nickname, books=[], is_empty=True)  # ✅ 서재가 없으면 is_empty=True 반환

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

# ✅ (4) 서재 상태 조회 (is_empty 반환)
@router.get("/library/{nickname}/status")
def check_library_status(nickname: str):
    library = library_collection.find_one({"nickname": nickname})
    if library and library.get("books", []):
        return {"nickname": nickname, "is_empty": False}
    return {"nickname": nickname, "is_empty": True}  # ✅ 서재가 비어있으면 True

# ✅ (5) 서재에 동화책 추가 (저자 제거, 캐릭터 리스트 추가)
@router.post("/library/{nickname}/books", response_model=Book)
def add_book(nickname: str, book: Book):
    library = library_collection.find_one({"nickname": nickname})
    if not library:
        raise HTTPException(status_code=404, detail="서재를 찾을 수 없습니다.")
    
    new_book = {"id": str(ObjectId()), "title": book.title, "characters": book.characters}
    library_collection.update_one({"nickname": nickname}, {"$push": {"books": new_book}})
    
    return Book(**new_book)

# ✅ (6) 서재의 특정 동화책 삭제
@router.delete("/library/{nickname}/books/{book_id}")
def delete_book(nickname: str, book_id: str):
    library = library_collection.find_one({"nickname": nickname})
    if not library:
        raise HTTPException(status_code=404, detail="서재를 찾을 수 없습니다.")

    updated_books = [book for book in library.get("books", []) if book["id"] != book_id]

    if len(updated_books) == len(library.get("books", [])):
        raise HTTPException(status_code=404, detail="책을 찾을 수 없습니다.")

    library_collection.update_one({"nickname": nickname}, {"$set": {"books": updated_books}})
    return {"message": "책이 삭제되었습니다."}

# ✅ (7) 서재의 특정 동화책에 캐릭터 추가
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

# ✅ (8) 서재의 특정 동화책 제목 변경
@router.patch("/library/{nickname}/books/{book_id}")
def update_book_title(nickname: str, book_id: str, book_data: UpdateBookTitle):
    library = library_collection.find_one({"nickname": nickname})
    if not library:
        raise HTTPException(status_code=404, detail="서재를 찾을 수 없습니다.")

    book_index = next((i for i, book in enumerate(library.get("books", [])) if book["id"] == book_id), None)
    if book_index is None:
        raise HTTPException(status_code=404, detail="책을 찾을 수 없습니다.")

    updated_books = library["books"]
    updated_books[book_index]["title"] = book_data.new_title  # ✅ 제목 변경

    library_collection.update_one({"nickname": nickname}, {"$set": {"books": updated_books}})
    return {"message": "책 제목이 수정되었습니다.", "new_title": book_data.new_title}

# ✅ (9) 사용자가 선택한 동화책 & 캐릭터 저장
@router.post("/library/{nickname}/selection")
def save_story_selection(nickname: str, selection: StorySelection):
    library = library_collection.find_one({"nickname": nickname})
    
    if not library:
        raise HTTPException(status_code=404, detail="서재를 찾을 수 없습니다.")

    library_collection.update_one(
        {"nickname": nickname},
        {"$set": {"selected_story": selection.story, "selected_character": selection.character}}
    )
    return {"message": "선택한 동화책과 캐릭터가 저장되었습니다."}

# ✅ (10) 사용자가 선택한 동화책 & 캐릭터 조회
@router.get("/library/{nickname}/selection")
def get_story_selection(nickname: str):
    library = library_collection.find_one({"nickname": nickname})
    if not library or "selected_story" not in library or "selected_character" not in library:
        raise HTTPException(status_code=404, detail="선택된 동화책과 캐릭터가 없습니다.")
    
    return {
        "story": library["selected_story"],
        "character": library["selected_character"]
    }