from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from config import  hashing, database, token

authentication_router = APIRouter(
  tags=['Authentication']
)

@authentication_router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends()):
  user = database.users_collection.find_one({"email": request.username})

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Invalid Credentials")
  if not hashing.Hash.verify(user["password"], request.password):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")
  access_token = token.create_access_token(data={"sub": user["email"]})
  return {"access_token": access_token, "token_type": "bearer"}