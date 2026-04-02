from pydantic import BaseModel

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