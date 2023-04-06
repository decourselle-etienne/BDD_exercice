import models
import factory
import database


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):

    id = factory.Faker('random_number')
    username = factory.Faker('name')
    email = factory.Faker('email')
    first_name = factory.Faker('name')
    last_name = factory.Faker('name')

    class Meta:
        model = models.User
        sqlalchemy_session = database.SessionLocal
        sqlalchemy_session_persistence = 'commit'


class PostFactory(factory.alchemy.SQLAlchemyModelFactory):

    id = factory.Faker('random_number')
    content = factory.Faker('sentence')
    user_id = factory.SubFactory(UserFactory)

    class Meta:
        model = models.Post
        sqlalchemy_session = database.SessionLocal
        sqlalchemy_session_persistence = 'commit'


class ReactionFactory(factory.alchemy.SQLAlchemyModelFactory):

    user_id = factory.SubFactory(UserFactory)
    post_id = factory.SubFactory(PostFactory)
    type = factory.Faker('name')

    class Meta:
        model = models.Reaction
        sqlalchemy_session = database.SessionLocal
        sqlalchemy_session_persistence = 'commit'
