from fastapi import FastAPI
import uvicorn
from sqlmodel import create_engine, SQLModel
from models.book_models import *
from models.user_models import *
import repos.book_repository


app = FastAPI()

#def create_db_and_tables():
#    SQLModel.metadata.create_all(engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/books")
async def books():
    books = repos.book_repository.select_all_books()
    return {'books': books}

@app.get("/book/{id}")
async def book(id):
    book = repos.book_repository.select_book(id)
    return book

if __name__ == "__main__":
#    create_db_and_tables()
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    