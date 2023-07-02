from pydantic import BaseModel


class PostCreate(BaseModel):

    title: str
    description: str


class PostEdit(BaseModel):

    title: str
    description: str
