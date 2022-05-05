from datetime import date
from typing import Optional
from pydantic import BaseModel

class Book(BaseModel):
  name: str
  page: str
  category: str
  author: str
  borrowed: bool = False
  delivery_date: Optional[str] = ""
  issue_date: Optional[str] = ""

class BorrowBook(BaseModel):
  borrowed: bool = True
  delivery_date: Optional[str] = ""
  issue_date: Optional[str] = ""


class ReturnBook(BaseModel):
  borrowed: bool = False
  delivery_date: Optional[str] = ""
  issue_date: Optional[str] = ""