from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, select
from .database import Base
from validate_email import validate_email
from http import HTTPStatus
from fastapi import HTTPException
from src.schemas.user import UserAuthenticate, UserCreate
from src.schemas.post import PostCreate
from src.utils.auth import AuthHandler
from datetime import datetime


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)

    posts = relationship('Post', back_populates='creator')

    @classmethod
    def create(cls, user: UserCreate, auth_handler: AuthHandler, db: Session):

        if not validate_email(user.email):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='email is not valid!'
            )

        if db.query(User.id).filter_by(username=user.username).first():
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='username already exists!'
            )

        if db.query(User.id).filter_by(email=user.email).first():
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='email already exists!'
            )

        user = User(
            email=user.email,
            username=user.username,
            password=auth_handler.get_hashed_password(user.password)
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @classmethod
    def get(cls, user: UserAuthenticate, auth_handler: AuthHandler, db: Session):

        user_instance = db.query(User.id).filter_by(email=user.email).first()
        if not user_instance:
            return HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='no such user'
            )
        if not auth_handler.verify_password(user.password, auth_handler.get_hashed_password(user.password)):
            return HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='wrong password'
            )
        return user_instance


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    creator = relationship('User', back_populates='posts', uselist=False)

    @classmethod
    def create(cls, post: PostCreate, user_id, db):

        post = Post(
            title=post.title,
            description=post.description,
            user_id=user_id
        )

        db.add(post)
        db.commit()
        db.refresh(post)

        return post
