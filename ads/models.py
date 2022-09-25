import json

from django.db import models


class Ads(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField(null=True)
    address = models.CharField(max_length=100)
    is_published = models.BooleanField(default=False)


class Categories(models.Model):
    name = models.CharField(max_length=600)



