import enum
from sqlalchemy import Column, ForeignKey, Integer, VARCHAR, Enum
from sqlalchemy.ext.declarative import declarative_base

# from database import Base

Base = declarative_base()


class TypeEnum(enum.Enum):
    like = "Like"
    dislike = "Dislike"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(VARCHAR(50), index=True, nullable=False)
    email = Column(VARCHAR(50), unique=True, index=True, nullable=False)
    first_name = Column(VARCHAR(50), index=True, nullable=False)
    last_name = Column(VARCHAR(50), index=True, nullable=False)


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(VARCHAR(250), index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))


class Reaction(Base):
    __tablename__ = "reactions"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
    type = Column(Enum(TypeEnum), index=True, nullable=False)
