import email
from pydantic import BaseModel

class User(BaseModel):
  email: str
  password: str
  type: str
  