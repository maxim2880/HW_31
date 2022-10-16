from django.contrib.auth.models import AbstractUser
from django.db import models


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
    role = models.CharField(max_length=50)
    age = models.IntegerField(null=True)
    location = models.ManyToManyField(Location)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['username']

    def __str__(self):
        return self.username
