from sqlalchemy.orm import Session

import models


def get_users(db: Session):
    users = db.query(models.User).all()

    for user in users:
        posts = db.query(models.Post).filter(
            user.id == models.Post.user_id).all()
        for post in posts:
            reactions = db.query(models.Reaction).filter(
                post.id == models.Reaction.post_id).all()
            post.reactions = reactions
        user.posts = posts

    return users


def get_posts(db: Session):
    posts = db.query(models.Post).all()
    for post in posts:
        reactions = db.query(models.Reaction).filter(
            post.id == models.Reaction.post_id).all()
        post.reactions = reactions
    return posts


def get_all(db: Session):
    users = db.query(models.User).all()
    posts = db.query(models.Post).all()
    reactions = db.query(models.Reaction).all()
    data = [{"Users": users}, {"Posts": posts}, {"Reactions": reactions}]
    return data


def add_reaction(db: Session, post_id: int, user_id: int, value: int):

    if value == 1:
        db_reaction = models.Reaction(
            user_id=user_id, post_id=post_id, type="Like")
        db.add(db_reaction)
        db.commit()
        db.refresh(db_reaction)
    if value == 2:
        db_reaction = models.Reaction(
            user_id=user_id, post_id=post_id, type="Dislike")
        db.add(db_reaction)
        db.commit()
        db.refresh(db_reaction)
    return db_reaction


def add_post(db: Session, content: str, user_id: int):
    db_post = models.Post(
        user_id=user_id, content=content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def modify_post(db: Session, post_id: int, content: str, user_id: int):
    db_post = db.query(models.Post).filter(
        post_id == models.Post.id).first()

    if db_post.user_id == user_id:
        new_db_post = models.Post(
            content=content, user_id=user_id)
        db.add(new_db_post)
        db.commit()
        db.refresh(new_db_post)
        return new_db_post
    else:
        return {"MODIFICATION NON AUTORISEE"}
