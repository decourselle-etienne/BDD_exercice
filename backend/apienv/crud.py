from sqlalchemy.orm import Session

import models
import schemas
import fake_data


def get_users(db: Session):
    return db.query(models.User).all()


def get_posts(db: Session):
    posts = db.query(models.Post).all()
    posts_reactions = db.query(models.Post).join(
        models.Reaction, models.Post.id == models.Reaction.post_id).all()
    return posts


def generate_data(db: Session):
    for _ in range(1500):
        db_user = fake_data.UserFactory._create(models.User)
        db_posts = fake_data.PostFactory._create(models.Post)
        db_reactions = fake_data.ReactionFactory._create(models.Reaction)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        db.add(db_posts)
        db.commit()
        db.refresh(db_posts)
        db.add(db_reactions)
        db.commit()
        db.refresh(db_reactions)
    message = {"message : database generated"}
    return message
