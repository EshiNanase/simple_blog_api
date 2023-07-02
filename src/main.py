from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src.schemas.user import UserCreate, UserAuthenticate
from src.schemas.post import PostCreate
from src.utils.auth import AuthHandler
from src.models.models import User, Post
from src.models.database import get_db
from http import HTTPStatus

app = FastAPI()
auth_handler = AuthHandler()


@app.get('/users/list', status_code=HTTPStatus.OK)
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@app.post('/users/create', status_code=HTTPStatus.CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return User.create(user, auth_handler, db)


@app.post('/users/token', status_code=HTTPStatus.OK)
def get_token(user: UserAuthenticate, db: Session = Depends(get_db)):
    user = User.get(user, auth_handler, db)
    return {'token': auth_handler.encode_token(user.id)}


@app.post('/posts/create', status_code=HTTPStatus.CREATED)
def create_post(post: PostCreate, user_id=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    return Post.create(post, user_id, db)


@app.get('/posts/list', status_code=HTTPStatus.OK)
def list_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()


@app.get('/posts/list/{user_id}', status_code=HTTPStatus.OK)
def list_user_posts(user_id: int, db: Session = Depends(get_db)):
    return db.query(Post).filter_by(user_id=user_id).all()
