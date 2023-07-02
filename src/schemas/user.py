from pydantic import BaseModel


class UserResponse(BaseModel):

    id: int
    email: str
    username: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):

    email: str
    username: str
    password: str


class UserAuthenticate(BaseModel):

    email: str
    password: str
