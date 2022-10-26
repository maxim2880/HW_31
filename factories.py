from datetime import date

import factory.django


class UserFactory(factory.django.DjangoModelFactory):
    first_name = 'test',
    last_name = 'test1',
    username = 'test_test',
    email = 'test@test.ru',
    password = '12345',
    birth_date = factory.Faker('date_object')

    class Meta:
        model = 'users.User'


class SelectionFactory(factory.django.DjangoModelFactory):
    name = 'test'
    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = 'ads.Selection'


class AdFactory(factory.django.DjangoModelFactory):
    name = 'Ad'
    author = factory.SubFactory(UserFactory)
    price = 1

    class Meta:
        model = 'ads.Ad'
