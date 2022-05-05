from fastapi import APIRouter, Depends, status
from config.database import books_collection, students_collection
from models.books_model import Book, BorrowBook, ReturnBook
from models.users_model import User
from schemas.book_schemas import books_serializer
from bson import ObjectId
from config.oauth2 import get_current_user

book_router = APIRouter(
  prefix="/book",
  tags=['Books']
)

@book_router.get('/', status_code=status.HTTP_200_OK)
async def get_books(current_user: User = Depends(get_current_user)):
  books = books_serializer(books_collection.find())
  return {"books": books}

@book_router.get('/{id}', status_code=status.HTTP_200_OK)
async def get_book(id: str, current_user: User = Depends(get_current_user)):
  book = books_serializer(books_collection.find({"_id": ObjectId(id)}))
  return {"book": book}

@book_router.post('/', status_code=status.HTTP_201_CREATED)
async def post_book(book: Book, current_user: User = Depends(get_current_user)):
  _id = books_collection.insert_one(dict(book))
  book = books_serializer(books_collection.find({"_id": _id.inserted_id}))
  return {"book": book}

@book_router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
async def update_book(id: str, book: Book, current_user: User = Depends(get_current_user)):
  books_collection.find_one_and_update({"_id": ObjectId(id)}, {
    "$set": dict(book)
  })
  book = books_serializer(books_collection.find({"_id": ObjectId(id)}))
  return {"book": book}

@book_router.put('/{book_id}/book_borrowed/{student_no}', status_code=status.HTTP_202_ACCEPTED)
async def book_borrowed(book_id: str, student_no: str, book: BorrowBook, current_user: User = Depends(get_current_user)):
  books_collection.find_one_and_update({"_id": ObjectId(book_id)}, {
    "$set": dict(book)
  })
  updated_book = books_serializer(books_collection.find({"_id": ObjectId(book_id)}))
  current_student = students_collection.find_one({"student_no": student_no})
  current_student["books"].append(updated_book[0])
  students_collection.find_one_and_update({"student_no": student_no}, {"$set": current_student})
  return {"book": updated_book}


@book_router.put('/{book_id}/book_returned/{student_no}', status_code=status.HTTP_202_ACCEPTED)
async def book_returned(book_id: str, student_no: str, book: ReturnBook, current_user: User = Depends(get_current_user)):
  books_collection.find_one_and_update({"_id": ObjectId(book_id)}, {
    "$set": dict(book)
  })
  updated_book = books_serializer(books_collection.find({"_id": ObjectId(book_id)}))
  current_student = students_collection.find_one({"student_no": student_no})

  for book in current_student["books"]:
    if book["id"] == updated_book[0]["id"]:
      removed_book = book
  current_student["books"].remove(removed_book)
  students_collection.find_one_and_update({"student_no": student_no}, {"$set": current_student})
  return {"book": updated_book}


@book_router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(id: str, current_user: User = Depends(get_current_user)):
  books_collection.find_one_and_delete({"_id": ObjectId(id)})
  return {"data": []}