from fastapi import APIRouter, status
from config import database, hashing
from models.users_model import User
from schemas.user_schemas import users_serializer
from bson import ObjectId

user_router = APIRouter(
  prefix="/user",
  tags=['Users']
)

@user_router.get('/', status_code=status.HTTP_200_OK)
async def get_users():
  users = users_serializer(database.users_collection.find())
  return {"users": users}

@user_router.get('/{id}', status_code=status.HTTP_200_OK)
async def get_user(id: str):
  user = users_serializer(database.users_collection.find({"_id": ObjectId(id)}))
  return {"user": user}

@user_router.post('/', status_code=status.HTTP_201_CREATED)
async def post_user(user: User):
  user.password = hashing.Hash.bcrypt(user.password)
  new_user = database.users_collection.insert_one(dict(user))
  created_user = users_serializer(database.users_collection.find({"_id": new_user.inserted_id}))
  return {"user": created_user}
