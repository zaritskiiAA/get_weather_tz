import factory
from django.contrib.auth import get_user_model

from users.models import UserQuery, UserHistory

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):

    username = factory.Faker('user_name')
    password = factory.Sequence(lambda x: 'test_password%d' % x)

    class Meta:
        model = User


class UserQueryFactory(factory.django.DjangoModelFactory):

    city = factory.Faker('city')
    latitude = factory.Faker('latitude')  
    longitude = factory.Faker('longitude')  

    @classmethod
    def _generate(cls, strategy, config, **kwargs):
        # Иногда faker генерирует города с пробелами в следствии чего
        # резулаты не совпадают из-за некоррекной кодировки
        user_query = super()._generate(strategy, config, **kwargs)
        user_query.city = user_query.city.replace(' ', '')
        user_query.save()
        return user_query

    class Meta:
        model = UserQuery


class UserHistoryFactory(factory.django.DjangoModelFactory):

    user = factory.SubFactory(UserFactory)
    query = factory.SubFactory(UserQueryFactory)

    class Meta:
        model = UserHistory