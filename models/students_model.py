from typing import List, Optional
from pydantic import BaseModel
from models.books_model import Book

class Student(BaseModel):
  first_name: str
  last_name: str
  student_no: str
  email: str
  password: str
  books: Optional[List[Book]] = []

class UpdatedStudent(BaseModel):
  first_name: str
  last_name: str
  student_no: str