from sqlmodel import Session, select

from db.db import engine
from models.user_models import User
from models.book_models import AvailableBooks, Book

def select_all_users():
    with Session(engine) as session:
        statement = select(User)
        res = session.exec(statement).all()
        return res


def find_user(name):
    with Session(engine) as session:
        statement = select(User).where(User.name == name)
        return session.exec(statement).first()

def select_user(id):
    with Session(engine) as session:
        statement = select(User).where(User.id == id)
        result = session.exec(statement)
        user = result.first()
        
        if user is None:
            return None
        
        obj = {
            "id": user.id,
            "name": user.name,
            "description": user.description,
        }

        statement = select(AvailableBooks.book_id).where(AvailableBooks.user_id == id)
        result = session.exec(statement)
        book_ids = result.all() 
        
        statement = select(Book).where(Book.id.in_(book_ids))
        result = session.exec(statement)
        books_that_user_has = result.all()

        book_data = []
        for book in books_that_user_has:
            book_data.append({"book_name": book.name, "book_id": book.id})

        obj["books"] = book_data
        return obj
        