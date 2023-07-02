from pydantic import BaseModel
from datetime import datetime


class PostResponseSingle(BaseModel):

    id: int
    title: str
    description: str
    user_id: int
    total_likes: int
    total_dislikes: int
    created_at: datetime

    class Config:
        orm_mode = True


class PostResponseMultiple(BaseModel):

    id: int
    title: str
    user_id: int

    class Config:
        orm_mode = True


class PostCreate(BaseModel):

    title: str
    description: str


class PostEdit(BaseModel):

    title: str
    description: str
