from database.session import engine, Base
from models.model import Book

Base.metadata.create_all(bind=engine)

print("table created")