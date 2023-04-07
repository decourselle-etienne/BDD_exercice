from sqlalchemy.orm import Session

import models


def get_users(db: Session):
    users = db.query(models.User, models.Post, models.Reaction, models.Report).filter(
        models.User.id == models.Post.user_id).filter(models.Post.id == models.Reaction.post_id).filter(models.User.id != models.Report.user_id).all()

    # for user in users:
    #     posts = db.query(models.Post).filter(
    #         user.id == models.Post.user_id)

    #     for post in posts:
    #         reactions = db.query(models.Reaction).filter(
    #             post.id == models.Reaction.post_id).all()
    #         post.reactions = reactions
    #     user.posts = posts

    return users


def get_users_reports(db: Session):
    reports = db.query(models.Report.user_id).all()
    users = []
    for report in reports:
        db_user = db.query(models.User).filter(
            report.user_id == models.User.id).first()
        if db_user in users:
            pass
        else:
            users.append(db_user)

    return users


def get_posts(db: Session):
    posts = db.query(models.Post).all()
    db_posts_reported = db.query(models.Report.post_id).all()

    for post in posts:
        count_reported = 0
        reactions = db.query(models.Reaction).filter(
            post.id == models.Reaction.post_id).all()
        post.reactions = reactions
        for reported in db_posts_reported:
            if post.id == reported.post_id:
                count_reported += 1
        post.reports = count_reported

    return posts


def get_reports(db: Session):
    reports = db.query(models.Report).all()
    for report in reports:
        reporter = db.query(models.User).filter(
            report.user_id == models.User.id).first()
        post = db.query(models.Post).filter(
            report.post_id == models.Post.id).first()
        report.reporter = reporter
        report.post = post
    return reports


def get_all(db: Session):
    users = db.query(models.User).all()
    posts = db.query(models.Post).all()
    reactions = db.query(models.Reaction).count()
    reports = db.query(models.Report).count()
    db_posts_reported = db.query(models.Report.post_id).all()
    db_reporter = db.query(models.Report.user_id).all()

    count_posts_reported = 0
    count_reporter = 0

    for post in posts:
        for post_reported in db_posts_reported:
            if post.id == post_reported.post_id:
                count_posts_reported += 1
                break

    for user in users:
        for reporter in db_reporter:
            if user.id == reporter.user_id:
                count_reporter += 1
                break

    data = [{"Users": len(users)}, {"Posts": len(posts)}, {
        "Reactions": reactions}, {"Reports": reports}, {"Posts Reported": count_posts_reported}, {"Reporter": count_reporter}]
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


def add_report(db: Session, reason: str, post_id: int, user_id: int):
    db_report = models.Report(
        user_id=user_id, reason=reason, post_id=post_id)
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


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


def delete_report(db: Session, post_id: int, user_id: int):
    db_report = db.query(models.Report).filter(user_id == models.Report.user_id).filter(
        post_id == models.Report.post_id).first()
    db.delete(db_report)
    db.commit()

    return {"Le report suivant a été supprimé :": db_report}
