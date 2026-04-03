from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError
import os

from auth_database.auth_dependecy import get_db
from auth_schemas.auth_schemas import UserCreate
from auth_models.auth_model import User
from auth_utils.auth_util import hash_password, verify_password
from auth_key import SECRET_KEY

app = FastAPI()

MY_SECRET_KEY = f"{SECRET_KEY}"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_TIME = 60

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(to_encode, key=MY_SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

@app.post("/signup")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pass = hash_password(user.password)

    new_user = User(
        username = user.username,
        email = user.email,
        hashed_password = hashed_pass,
        role = user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return {'id': new_user.id, 'username': new_user.username, 'email': new_user.email, 'role': new_user.role}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token_data = {'sub': user.username, 'role': user.role}
    token = create_access_token(token_data)
    return {
        'access_token': token,
        'token_type': 'bearer'
    }

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, MY_SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get('sub')
        role: str = payload.get('role')
        if username is None or role is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception

    return {'username': username, 'role': role}

@app.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"Message": f"Hello, {current_user['username']} | You are accessed protected route"}

def require_roles(allowed_roles: list[str]):
    def role_checker(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("role")
        # print(user_role)
        if user_role not in allowed_roles:
            # print(allowed_roles)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker

@app.get("/profile")
def profile(current_user: dict = Depends(require_roles(["qa", "admin"]))):
    return {"Message": f"Profile of {current_user['username']} ({current_user['role']})"}

@app.get("/user/dashboard")
def user_dashboard(current_user: dict = Depends(require_roles(['qa']))):
    return {"Message": "Welcome qa"}

@app.get("/admin/dashboard")
def admin_dashboard(current_user: dict = Depends(require_roles(['admin']))):
    return {"Message": "Welcome Admin"}