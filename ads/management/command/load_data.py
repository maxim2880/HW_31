from django.core.management.base import BaseCommand
import json
from ads.models import Ad, Categories


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('../data/categories.json', 'rb') as f:
            cat_data = json.load(f)

        for i in cat_data:
            cat = Categories()
            cat.name = cat_data["name"]
            cat.save()

        with open('../data/ads.json', 'rb') as f:
            adv_data = json.load(f)

        for i in adv_data:
            advertise = Ad()
            advertise.name = adv_data["name"]
            advertise.author = adv_data["author"]
            advertise.price = adv_data["price"]
            advertise.description = adv_data["description"]
            advertise.address = adv_data["address"]
            advertise.is_published = adv_data["is_published"]
            advertise.save()


