from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from datetime import timedelta, date
from dateutil.relativedelta import relativedelta

USER_MIN_AGE = 9


def birth_date_validator(value):
    diff_years = relativedelta(date.today(), value).years()
    if diff_years < USER_MIN_AGE:
        raise ValidationError('User is underage')
    return value

class Location(models.Model):
    name = models.CharField(max_length=150, unique=True)
    lat = models.FloatField(max_length=20)
    lng = models.FloatField(max_length=20)

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self):
        return self.name


# class User(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     username = models.CharField(max_length=50)
#     password = models.CharField(max_length=50)
#     role = models.CharField(max_length=50)
#     age = models.IntegerField(null=True)
#     location = models.ManyToManyField(Location)
#
#     class Meta:
#         verbose_name = "Пользователь"
#         verbose_name_plural = "Пользователи"
#         ordering = ['username']
#
#     def __str__(self):
#         return self.username


class UserRoles:
    USER = 'member'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    choices = (
        (USER, "Пользователь"),
        (ADMIN, "Админ"),
        (MODERATOR, "Модератов"),
    )


class User(AbstractUser):
    role = models.CharField(max_length=12, choices=UserRoles.choices, default='member')
    age = models.PositiveSmallIntegerField(null=True)
    location = models.ManyToManyField(Location)
    birth_date = models.DateField(validators=[birth_date_validator])
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['username']

    def __str__(self):
        return self.username
