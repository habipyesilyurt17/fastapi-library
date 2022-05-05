from pymongo import MongoClient

client = MongoClient("mongodb+srv://habip:MYXcSjEemmBbafko@cluster0.l0dja.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = client.fastapi_library
books_collection = db["books"]
students_collection = db["students"]
users_collection = db["users"]