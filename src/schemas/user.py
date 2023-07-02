from pydantic import BaseModel


class UserCreate(BaseModel):

    email: str
    username: str
    password: str


class UserAuthenticate(BaseModel):

    email: str
    password: str
