from pydantic import BaseModel


class PostBase(BaseModel):
    content: str


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class ReactionBase(BaseModel):
    type: str


class ReactionCreate(ReactionBase):
    pass


class Reaction(ReactionBase):
    user_id: int
    post_id: int

    class Config:
        orm_mode = True
