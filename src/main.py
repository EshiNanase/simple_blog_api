from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas.user import UserCreate, UserAuthenticate
from src.schemas.post import PostCreate, PostEdit
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
    user = User.login(user, auth_handler, db)
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


@app.put('/posts/edit/{post_id}', status_code=HTTPStatus.ACCEPTED)
def edit_post(post_id: int, edited_post: PostEdit, user_id=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    post = Post.get(post_id, db)
    user = User.get(user_id, db)
    if post.user_id != user.id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='you cant edit other peoples posts'
        )
    post.title = edited_post.title
    post.description = edited_post.description
    db.commit()
    db.refresh(post)
    return post


@app.delete('/posts/delete/{post_id}', status_code=HTTPStatus.ACCEPTED)
def delete_post(post_id: int, user_id=Depends(auth_handler.auth_wrapper), db: Session = Depends(get_db)):
    post = Post.get(post_id, db)
    user = User.get(user_id, db)
    if post.user_id != user.id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='you cant delete other peoples posts'
        )
    db.delete(post)
    db.commit()
    return post
