from pydantic import BaseModel
from sqlalchemy import Column, Integer, VARCHAR
from database.session import Base

class Student(BaseModel):
    name: str
    age: int
    roll: int

class Book(BaseModel):
    id: int
    title : str
    author : str
    publish_date : str

class Update_Book(BaseModel):
    title: str
    author: str
    publish_date: str

class Book_Table(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(VARCHAR(255))
    author = Column(VARCHAR(255))
    publish_date = Column(VARCHAR(255))

class BookStore(BaseModel):
    id: int
    title: str
    author: str
    publish_date: str
