from sqlmodel import create_engine
from secret import db_path #Путь до БД. СЕКРЕТНЫЙ ФАЙЛ

engine = create_engine(f"sqlite:///{db_path}", echo=True)