from db.db import engine
from models.book_models import *
from models.user_models import User
from sqlmodel import Session, select

def select_all_books():
    with Session(engine) as session:
        statement = select(Book)
        result = session.exec(statement)
        res = []
        for book in result:
            res.append({"id": book.id, 
                        "name": book.name, 
                        "author": book.author})
        return res
    
def select_book(id: int):
    with Session(engine) as session:
        statement = select(Book).where(Book.id == id)
        result = session.exec(statement)
        book = result.first()
        
        if book is None:
            return None
        
        obj = {
            "id": book.id,
            "name": book.name,
            "author": book.author,
            "description": book.description,
        }

        statement = select(AvailableBooks.user_id).where(AvailableBooks.book_id == id)
        result = session.exec(statement)
        user_ids = result.all() 
        
        statement = select(User).where(User.id.in_(user_ids))
        result = session.exec(statement)
        users_who_have_it = result.all()

        user_data = []
        for user in users_who_have_it:
            user_data.append({"user_name": user.name, "user_id": user.id})

        obj["who_has_it"] = user_data
        return obj

