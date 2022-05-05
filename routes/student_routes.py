from fastapi import APIRouter, status, Depends
from config import database, hashing, oauth2
from models.students_model import Student, UpdatedStudent
from schemas import student_schemas, user_schemas
from bson import ObjectId

student_router = APIRouter(
  prefix="/student",
  tags=['Students']
)

@student_router.get('/', status_code=status.HTTP_200_OK)
async def get_students():
  students = student_schemas.students_serializer(database.students_collection.find())
  return {"students": students}

@student_router.get('/{id}', status_code=status.HTTP_200_OK)
async def get_student(id: str):
  student = student_schemas.students_serializer(database.students_collection.find({"_id": ObjectId(id)}))
  return {"student": student}

@student_router.post('/', status_code=status.HTTP_201_CREATED)
async def post_student(student: Student):
  student.password = hashing.Hash.bcrypt(student.password)
  new_student = database.students_collection.insert_one(dict(student))
  created_student = student_schemas.students_serializer(database.students_collection.find({"_id": new_student.inserted_id}))
  user = {
    "email": created_student[0]["email"],
    "password": created_student[0]["password"],
    "type": "student"
  }
  new_user = database.users_collection.insert_one(dict(user))
  created_user = user_schemas.users_serializer(database.users_collection.find({"_id": new_user.inserted_id}))
  return {"student": created_student, "user": created_user}

@student_router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
async def update_student(id: str, student: UpdatedStudent):
  database.students_collection.find_one_and_update({"_id": ObjectId(id)}, {
    "$set": dict(student)
  })
  student = student_schemas.students_serializer(database.students_collection.find({"_id": ObjectId(id)}))
  return {"student": student}