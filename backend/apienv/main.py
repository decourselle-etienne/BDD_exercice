from fastapi import Depends, FastAPI, Path, Body
from sqlalchemy.orm import Session
from typing import Annotated


import crud
import schemas
from database import SessionLocal

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Ajouter un nouveau post
@app.post("/${user_id}/posts")
async def add_post(content: Annotated[str, Body(embed=True)], user_id: int, db: Session = Depends(get_db)):
    new_post = crud.add_post(
        db, user_id=user_id, content=content)
    return new_post


# Ajouter une nouvelle reaction
@app.post("/${user_id}/posts/${post_id}/reactions/${value}")
async def add_reaction(post_id: int, user_id: int, value: int, db: Session = Depends(get_db)):
    new_reaction = crud.add_reaction(
        db, post_id=post_id, user_id=user_id, value=value)
    return new_reaction


# Afficher tous les users, tous les posts et toutes les réactions séparément
@app.get("/all")
async def get_all(db: Session = Depends(get_db)):
    data = crud.get_all(db)
    return data


# Afficher tous les posts avec leur réactions associées
@app.get("/posts")
def read_items(db: Session = Depends(get_db)):
    items = crud.get_posts(db)
    return items


# Afficher tous les users avec leur posts et leurs réactions réalisées
@app.get("/users")
def read_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return users


# Modifier le content d'un post (avec user_id, post_id et content) >> réalisable uniquement si on est le créateur du post
@app.patch("/${user_id}/posts/${post_id}")
async def modify_post(content: Annotated[str, Body(embed=True)], user_id: int, post_id: int, db: Session = Depends(get_db)):
    modify_post = crud.modify_post(
        db, user_id=user_id, post_id=post_id, content=content)
    return modify_post
