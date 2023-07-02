from sqlalchemy.orm import relationship, Session, deferred
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from .database import Base
from validate_email import validate_email
from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.ext.hybrid import hybrid_property
from src.schemas.user import UserAuthenticate, UserCreate
from src.schemas.post import PostCreate
from src.utils.auth import AuthHandler
from datetime import datetime

user_post_likes = Table(
    'user_post_likes',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('post_id', Integer, ForeignKey('posts.id'))
)

user_post_dislikes = Table(
    'user_post_dislikes',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('post_id', Integer, ForeignKey('posts.id'))
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = deferred(Column(String, nullable=False))
    liked_posts = relationship('Post', secondary=user_post_likes, back_populates='liked_by')
    disliked_posts = relationship('Post', secondary=user_post_dislikes, back_populates='disliked_by')

    @classmethod
    def create(cls, user: UserCreate, auth_handler: AuthHandler, db: Session):

        if not validate_email(user.email):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='email is not valid!'
            )

        if db.query(User).filter_by(username=user.username).first():
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='username already exists!'
            )

        if db.query(User).filter_by(email=user.email).first():
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
    def login(cls, user: UserAuthenticate, auth_handler: AuthHandler, db: Session):
        user = db.query(User).filter_by(email=user.email).first()
        if not user:
            return HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='no such user'
            )
        if not auth_handler.verify_password(user.password, auth_handler.get_hashed_password(user.password)):
            return HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='wrong password'
            )
        return user

    @classmethod
    def get(cls, user_id: int, db: Session):

        user = db.query(User).filter_by(id=user_id).first()
        if not user:
            return HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='no such user'
            )
        return user


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    liked_by = relationship('User', secondary=user_post_likes, back_populates='liked_posts')
    disliked_by = relationship('User', secondary=user_post_dislikes, back_populates='disliked_posts')

    @hybrid_property
    def total_likes(self):
        return len(self.liked_by)

    @hybrid_property
    def total_dislikes(self):
        return len(self.disliked_by)

    def like(self, user: User, db: Session):

        if self.user_id == user.id:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='you cant like your own post'
            )

        if user in self.liked_by:
            self.liked_by.remove(user)
            db.commit()
            return

        if user in self.disliked_by:
            self.disliked_by.remove(user)

        self.liked_by.append(user)
        db.commit()

    def dislike(self, user: User, db: Session):

        if self.user_id == user.id:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='you cant dislike your own post'
            )

        if user in self.disliked_by:
            self.disliked_by.remove(user)
            db.commit()
            return

        if user in self.liked_by:
            self.liked_by.remove(user)

        self.disliked_by.append(user)
        db.commit()

    @classmethod
    def create(cls, post: PostCreate, user_id: int, db: Session):

        post = Post(
            title=post.title,
            description=post.description,
            user_id=user_id
        )

        db.add(post)
        db.commit()
        db.refresh(post)

        return post

    @classmethod
    def get(cls, post_id: int, db: Session):

        post = db.query(Post).filter_by(id=post_id).first()

        if not post:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='no such post'
            )

        return post
