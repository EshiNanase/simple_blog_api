from sqlalchemy.orm import relationship
from sqlalchemy.sql import exists
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from .database import Base
from validate_email import validate_email
from http import HTTPStatus
from fastapi import HTTPException


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)

    posts = relationship('Post', back_populates='creator')

    @classmethod
    def is_valid(self, db, user):

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


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    creator = relationship('User', back_populates='posts', uselist=False)
