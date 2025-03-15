from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str = ""
    description: str = ""
