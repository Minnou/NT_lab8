from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class AvailableBooks(SQLModel, table=True):
    book_id: Optional[int] = Field(default=None, foreign_key="book.id", primary_key=True)
    book: Optional['Book'] = Relationship(back_populates='availablebooks')
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    user: Optional['User'] = Relationship(back_populates='availablebooks')

class Book(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    availablebooks: Optional[AvailableBooks] = Relationship(back_populates='book')
    name: str = ""
    description: str = ""
    author: str = ""




    
