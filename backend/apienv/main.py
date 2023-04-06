from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

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


# generate data
@app.post("/generate")
async def generate_data():
    db_gen = get_db()
    db = next(db_gen)
    data = crud.generate_data(db)
    return data


# test
@app.get("/")
async def root():
    return {"message": "Hello World"}


# Ajouter un nouveau post
@app.post("/posts")
async def root():
    return {"message": "Hello World"}


# Ajouter une nouvelle reaction
@app.post("/posts/${post_id}/reactions")
async def root():
    return {"message": "Hello World"}


# Afficher tous les users, tous les posts et toutes les réactions séparément
@app.get("/all")
async def root():
    return {"message": "Hello World"}


# Afficher tous les posts avec leur réactions associées

@app.get("/posts/", response_model=list[schemas.Post])
def read_items(db: Session = Depends(get_db)):
    items = crud.get_posts(db)
    return items


# Afficher tous les users avec leur posts et leurs réactions réalisées
@app.get("/users/", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return users


# Modifier le content d'un post (avec user_id, post_id et content) >> réalisable uniquement si on est le créateur du post
@app.patch("/posts/${post_id}")
async def root():
    return {"message": "Hello World"}
