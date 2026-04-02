from fastapi import FastAPI, HTTPException
from typing import Optional

from models.model import Student, Book, Update_Book
from crud.crud import Books

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/greet/{name}")
def greet(name: str, age: Optional[int] = None):
    return {"message": f"Hello,{name} Welcome to FastAPI and {age}"}

@app.post("/student")
def create_student(student: Student):
    return {
        "name": student.name,
        "age": student.age,
        "roll": student.roll
    }

@app.get("/book")
def get_book():
    return Books

@app.get("/book/{id}")
def get_book_by_id(id : int):
    for book in Books:
        if book["id"] == id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/book")
def add_book(book : Book):
    new_book = book.model_dump()
    Books.append(new_book)
    return "Book added successfully"

@app.put("/book/{id}")
def update_book(id: int, book_update: Update_Book):
    for book in Books:
        if book["id"] == id:
            book["title"] = book_update.title
            book["author"] = book_update.author
            book["publish_date"] = book_update.publish_date

            return "Book updated successfully"
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/book/{id}")
def delete_book(id: int):
    for book in Books:
        if book["id"] == id:
            Books.remove(book)
            return "Book deleted successfully"
    raise HTTPException(status_code=404, detail="Book not found")