from typing import List, Dict, Union

from fastapi import APIRouter, Security, security, Depends, Query
from fastapi.security import HTTPAuthorizationCredentials
from sqlmodel import select
from starlette.responses import JSONResponse
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
from fastapi.encoders import jsonable_encoder
import repos.book_repository
from models.book_models import *
from db.db import session
from endpoints.user_endpoints import auth_handler

book_router = APIRouter()

@book_router.get("/books", tags=["Books"])
async def books():
    books = repos.book_repository.select_all_books()
    if not books:
        return JSONResponse(status_code=HTTP_404_NOT_FOUND)
    
    return {'books': books}

@book_router.get("/book/{id}", tags=["Books"])
async def book(book_id: int):
    book = repos.book_repository.select_book(book_id)
    if not book:
        return JSONResponse(status_code=HTTP_404_NOT_FOUND, content={"detail": "Book not found"})
    return book

@book_router.post("/books", tags=["Books"])
async def books(book_properties: Book, user=Depends(auth_handler.get_current_user)):
    book = Book(name=book_properties.name, description=book_properties.description, author=book_properties.author)
    session.add(book)
    session.commit()
    return book_properties

@book_router.patch("/books/{id}", response_model=Book, tags=["Books"])
async def books(book_id: int, book_properties: Book, user=Depends(auth_handler.get_current_user)):
    book_found = session.get(Book, book_id)
    if not book:
        return JSONResponse(status_code=HTTP_404_NOT_FOUND, content={"detail": "Book not found"})
    update_item = book_properties.model_dump(exclude_unset=True)
    update_item.pop('id', None)
    for key, val in update_item.items():
        book_found.__setattr__(key, val)
    session.commit()
    return update_item

@book_router.delete("/books/{id}", status_code=HTTP_204_NO_CONTENT, tags=["Books"])
async def books(book_id: int, user=Depends(auth_handler.get_current_user)):
    book_found = session.get(Book, book_id)
    if not book_found:
        return JSONResponse(status_code=HTTP_404_NOT_FOUND, content={"detail": "Book not found"})
    session.delete(book_found)
    session.commit()

@book_router.post("/availablebooks", tags=["Books", "Users"])
async def availablebooks(book_id: int, user_id: int, user=Depends(auth_handler.get_current_user)):
    available_book = AvailableBooks(book_id=book_id, user_id=user_id)
    session.add(available_book)
    session.commit()
    return available_book

@book_router.delete("/availablebooks/{book_id}:{user_id}", status_code=HTTP_204_NO_CONTENT, tags=["Books", "Users"])
async def availablebooks(book_id: int, user_id: int, user=Depends(auth_handler.get_current_user)):
    statement = select(AvailableBooks).where(AvailableBooks.book_id==book_id).where(AvailableBooks.user_id==user_id)
    available_book = session.exec(statement).first()
    if not available_book:
        return JSONResponse(status_code=HTTP_404_NOT_FOUND, content={"detail": "User/book not found"})
    session.delete(available_book)
    session.commit()