from fastapi import Depends, FastAPI, Path, Body
from sqlalchemy.orm import Session
from typing import Annotated

import fake_data
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


@app.post('/seed')
def seed_data():
    fake_data.seed_users()
    fake_data.seed_posts()
    fake_data.seed_reactions()
    fake_data.seed_reports()
    return {"message": "Data seeded"}


# Ajouter un nouveau post
@app.post("/${user_id}/posts")
async def add_post(content: Annotated[str, Body(embed=True)], user_id: int, db: Session = Depends(get_db)):
    new_post = crud.add_post(
        db, user_id=user_id, content=content)
    return new_post


# Ajouter une nouvelle reaction
@app.post("/${user_id}/posts/${post_id}/reactions/${value}")
async def add_report(value: int, post_id: int, user_id: int, db: Session = Depends(get_db)):
    new_reaction = crud.add_report(
        db, post_id=post_id, user_id=user_id, value=value)
    return new_reaction


# Ajouter un nouveau report
@app.post("/${user_id}/posts/${post_id}/reports")
async def add_reaction(user_id: int, post_id: int,  reason: Annotated[str, Body(embed=True)], db: Session = Depends(get_db)):
    new_report = crud.add_reaction(
        db, post_id=post_id, user_id=user_id, reason=reason)
    return new_report


# Afficher le total d'users, de posts, de réactions, de reports, de posts avec report et de reporter
@app.get("/all")
async def get_all(db: Session = Depends(get_db)):
    data = crud.get_all(db)
    return data


# Afficher tous les posts avec leur réactions associées et leur nombre de report
@app.get("/posts")
def get_post(db: Session = Depends(get_db)):
    posts = crud.get_posts(db)
    return posts


# Afficher tous les reports avec leur Reporter et Post visé
@app.get("/reports")
def get_reports(db: Session = Depends(get_db)):
    reports = crud.get_reports(db)
    return reports


# Afficher tous les users avec leur posts et leurs réactions réalisées en excluant les posts avec au moins 1 report
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return users


# Afficher tous les users qui ont réalisé au moins 1 report
@app.get("/users/reports")
def read_users_reports(db: Session = Depends(get_db)):
    users = crud.get_users_reports(db)
    return users


# Modifier le content d'un post (avec user_id, post_id et content) >> réalisable uniquement si on est le créateur du post
@app.patch("/${user_id}/posts/${post_id}")
async def modify_post(content: Annotated[str, Body(embed=True)], user_id: int, post_id: int, db: Session = Depends(get_db)):
    modify_post = crud.modify_post(
        db, user_id=user_id, post_id=post_id, content=content)
    return modify_post

# Supprimer un report


@app.delete("/${user_id}/posts/${post_id}/reports")
async def delete_report(user_id: int, post_id: int, db: Session = Depends(get_db)):
    delete_report = crud.delete_report(
        db, user_id=user_id, post_id=post_id)
    return delete_report
