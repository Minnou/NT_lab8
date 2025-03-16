from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str = Field(index=True)
    description: str = ""
    password: str = Field(max_length=256, min_length=6)
    availablebooks: Optional['AvailableBooks'] = Relationship(back_populates='user')
