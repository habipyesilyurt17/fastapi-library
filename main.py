from fastapi import FastAPI
from routes.student_routes import student_router
from routes.user_routes import user_router
from routes.book_routes import book_router
from routes.authentication_routes import authentication_router

app = FastAPI()

app.include_router(authentication_router)
app.include_router(user_router)
app.include_router(book_router)
app.include_router(student_router)