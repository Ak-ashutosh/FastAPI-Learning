from auth_database.auth_session import engine, Base
from auth_models.auth_model import User

Base.metadata.create_all(bind=engine)

print("table created")