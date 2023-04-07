import models
import database
import faker
from faker_enum import EnumProvider
import random

db = database.SessionLocal()
fake = faker.Faker()
fake.add_provider(EnumProvider)


def seed_users():
    num_users = 1500

    for _ in range(num_users):
        user = models.User(username=fake.unique.user_name(),
                           first_name=fake.first_name(),
                           last_name=fake.last_name(),
                           email=fake.unique.email())
        db.add(user)

    db.commit()


def seed_posts():
    users = db.query(models.User).all()
    num_posts_per_user = 10

    for user in users:
        for _ in range(num_posts_per_user):
            post = models.Post(content=fake.text(max_nb_chars=140),
                               user_id=user.id)
            db.add(post)

    db.commit()


def seed_reactions():
    posts = db.query(models.Post).all()
    num_reactions_per_post = 10
    num_users = 1500

    for post in posts:
        users = random.sample(
            range(1, num_users + 1), num_reactions_per_post)
        for user_id in users:
            reaction = models.Reaction(type=fake.enum(models.TypeEnum),
                                       user_id=user_id,
                                       post_id=post.id)
            db.add(reaction)

    db.commit()


def seed_reports():
    posts = db.query(models.Post).all()
    length = len(posts)
    num_users = 1500

    for _ in range(1000):
        post = random.randint(1, length)
        user = random.randint(1, num_users)

        report = models.Report(reason=fake.text(max_nb_chars=250),
                               user_id=user,
                               post_id=post)
        db.add(report)

    db.commit()
