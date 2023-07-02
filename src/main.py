from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src.schemas.user import UserCreate
from src.utils.user import create_user_with_hashed_password, get_all_users
from src.models.database import get_db

app = FastAPI()


@app.get('/users/list')
def list_users(db: Session = Depends(get_db)):
    return get_all_users(db)


@app.post('/users/create')
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user_with_hashed_password(db, user)
