from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
import uvicorn
from sqlmodel import create_engine, SQLModel, Session, select
from models.book_models import *
from models.user_models import *
import repos.book_repository
from db.db import engine


app = FastAPI()
session = Session(bind=engine)
#def create_db_and_tables():
#    SQLModel.metadata.create_all(engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/books")
async def books():
    books = repos.book_repository.select_all_books()
    if not books:
        return JSONResponse(status_code=HTTP_404_NOT_FOUND)
    
    return {'books': books}

@app.get("/book/{id}")
async def book(book_id: int):
    book = repos.book_repository.select_book(book_id)
    if not book:
        return JSONResponse(status_code=HTTP_404_NOT_FOUND, content={"detail": "Book not found"})
    return book

@app.post("/books")
async def books(book_properties: Book):
    book = Book(name=book_properties.name, description=book_properties.description, author=book_properties.author)
    session.add(book)
    session.commit()
    return book_properties

@app.patch("/books{id}", response_model=Book)
async def books(book_id: int, book_properties: Book):
    book_found = session.get(Book, book_id)
    if not book:
        return JSONResponse(status_code=HTTP_404_NOT_FOUND, content={"detail": "Book not found"})
    update_item = book_properties.model_dump(exclude_unset=True)
    update_item.pop('id', None)
    for key, val in update_item.items():
        book_found.__setattr__(key, val)
    session.commit()
    return update_item

@app.delete("/books{id}", status_code=HTTP_204_NO_CONTENT)
async def books(book_id: int):
    book_found = session.get(Book, book_id)
    if not book_found:
        return JSONResponse(status_code=HTTP_404_NOT_FOUND, content={"detail": "Book not found"})
    session.delete(book_found)
    session.commit()

@app.post("/availablebooks")
async def availablebooks(book_id: int, user_id: int):
    availablebook = AvailableBooks(book_id=book_id, user_id=user_id)
    session.add(availablebook)
    session.commit()
    return availablebook

if __name__ == "__main__":
#    create_db_and_tables()
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    session.close()
    