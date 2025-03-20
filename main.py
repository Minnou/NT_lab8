from fastapi import FastAPI
import uvicorn
from endpoints.book_endpoints import book_router
from endpoints.user_endpoints import user_router
from db.db import session

app = FastAPI()
#session = Session(bind=engine)
app.include_router(book_router)
app.include_router(user_router)

#def create_db_and_tables():
#    SQLModel.metadata.create_all(engine)



if __name__ == "__main__":
#    create_db_and_tables()
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
