import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Categories, Ads


def index(request):
    return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class CategoryView(View):

    def get(self, request):
        categories = Categories.objects.all()

        response = []
        for category in categories:
            response.append({
                "id": category.id,
                "name": category.name
            })

        return JsonResponse(response, safe=False, status=200)

    def post(self, request):
        category_data = json.loads(request.body)
        category = Categories()
        category.name = category_data["name"]

        category.save()

        return JsonResponse({
            "id": category.id,
            "name": category.name
        })


class CategoryDetailView(DetailView):
    model = Categories

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        return JsonResponse({
            "id": category.id,
            "name": category.name
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdsView(View):
    def get(self, request):
        advertises = Ads.objects.all()

        response = []
        for advertise in advertises:
            response.append({
                "id": advertise.id,
                "name": advertise.name,
                "author": advertise.author,
                "price": advertise.price,
                "description": advertise.description,
                "address": advertise.address,
                "is_published": advertise.is_published
            })

        return JsonResponse(response, safe=False, status=200)

    def post(self, request):
        adv_data = json.loads(request.body)
        advertise = Ads()
        advertise.name = adv_data["name"]
        advertise.author = adv_data["author"]
        advertise.price = adv_data["price"]
        advertise.description = adv_data["description"]
        advertise.address = adv_data["address"]
        advertise.is_published = adv_data["is_published"]

        return JsonResponse({
            "id": advertise.id,
            "name": advertise.name,
            "author": advertise.author,
            "price": advertise.price,
            "description": advertise.description,
            "address": advertise.address,
            "is_published": advertise.is_published
        })


class AdsDetailView(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        advertise = self.get_object()

        return JsonResponse({
            "id": advertise.id,
            "name": advertise.name,
            "author": advertise.author,
            "price": advertise.price,
            "description": advertise.description,
            "address": advertise.address,
            "is_published": advertise.is_published
        })
