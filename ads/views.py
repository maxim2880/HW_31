import json

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count, Avg
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Categories, Ads, User, Location


def index(request):
    return JsonResponse({"status": "ok"}, status=200)


# Представления категорий

class CategoryListView(ListView):
    model = Categories

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by("name")

        response = []
        for category in self.object_list:
            response.append({
                "id": category.id,
                "name": category.name
            })

        return JsonResponse(response, safe=False, status=200)


class CategoryDetailView(DetailView):
    model = Categories

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        return JsonResponse({
            "id": category.id,
            "name": category.name
        })


@method_decorator(csrf_exempt, name="dispatch")
class CategoryCreateView(CreateView):
    model = Categories
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)
        category = Categories.objects.create(
            name=category_data["name"]
        )

        return JsonResponse({
            "id": category.id,
            "name": category.name
        })


@method_decorator(csrf_exempt, name="dispatch")
class CategoryUpdateView(UpdateView):
    model = Categories
    fields = ["name"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        category_data = json.loads(request.body)

        self.object.name = category_data["name"]

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name
        })


@method_decorator(csrf_exempt, name="dispatch")
class CategoryDeleteView(DeleteView):
    model = Categories
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


# Представления объявлений

class AdsListView(ListView):
    model = Ads

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        # Пагинация

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        self.object_list = self.object_list.select_related("user").order_by("-price")

        advertises = []
        for advertise in page_obj:
            advertises.append({
                "id": advertise.id,
                "name": advertise.name,
                "author": advertise.author_id,
                "price": advertise.price,
                "description": advertise.description,
                "is_published": advertise.is_published,
                "image": advertise.image.url,
                "category": advertise.category_id
            })
        response = {
            "items": advertises,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }
        return JsonResponse(response, safe=False, status=200)


class AdsDetailView(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        advertise = self.get_object()

        return JsonResponse({
            "id": advertise.id,
            "name": advertise.name,
            "author": advertise.author_id,
            "price": advertise.price,
            "description": advertise.description,
            "is_published": advertise.is_published,
            "image": advertise.image.url if advertise.image else None,
            "category": advertise.category_id
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdsCreateView(CreateView):
    model = Ads
    fields = ["name", "author", "price", "description", "is_published", "image", "category"]

    def post(self, request, *args, **kwargs):
        adv_data = json.loads(request.body)
        advertise = Ads.objects.create(
            name=adv_data["name"],

            price=adv_data["price"],
            description=adv_data["description"],
            is_published=adv_data["is_published"],
            image=adv_data["image"],
            category_id=adv_data["category_id"]
        )

        advertise.author_id = get_object_or_404(User, pk=adv_data["author_id"])
        advertise.save()

        return JsonResponse({
            "id": advertise.id,
            "name": advertise.name,
            "author": advertise.author_id,
            "price": advertise.price,
            "description": advertise.description,
            "is_published": advertise.is_published,
            "image": advertise.image.url if advertise.image else None,
            "category": advertise.category_id
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdsUpdateView(UpdateView):
    model = Ads
    fields = ["name", "author", "price", "description", "is_published", "image", "category"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        adv_data = json.loads(request.body)

        self.object.name = adv_data["name"]
        self.object.author_id = adv_data["author_id"]
        self.object.price = adv_data["price"]
        self.object.description = adv_data["description"]
        self.object.is_published = adv_data["is_published"]
        self.object.image = adv_data["image"]
        self.object.category_id = adv_data["category_id"]

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author_id,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "image": self.object.image.url if self.object.image else None,
            "category": self.object.category_id
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdsDeleteView(DeleteView):
    model = Ads
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


# Работа с картинками

@method_decorator(csrf_exempt, name="dispatch")
class AdsImageView(UpdateView):
    model = Ads
    field = ["name", "author", "price", "description", "is_published", "image", "category"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES["image"]
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author_id,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "image": self.object.image.url if self.object.image else None,
            "category": self.object.category_id
        })


# Предстваления для пользователей и локаций

class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        # Пагинация

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        users = []
        for user in page_obj:
            users.append({
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "age": user.age,
                "location": list(map(str, user.location.all()))
            })

        response = {
            "items": users,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }
        return JsonResponse(response, safe=False, status=200)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()

        return JsonResponse({
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "age": user.age,
            "location": list(map(str, user.location.all()))
        })


@method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateView):
    model = User
    fields = ["username", "first_name", "last_name", "role", "age", "password", "location"]

    def post(self, request, *args, **kwargs):
        # super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)

        user = User.objects.create(
            username=user_data["username"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            password=user_data["password"],
            role=user_data["role"],
            age=user_data["age"],
        )

        for location in user_data["location"]:
            location_obj, created = Location.objects.get_or_create(name=location, defaults={
                "lat": "55",
                "lng": "55"
            })
            user.location.add(location_obj)
        user.save()

        return JsonResponse({
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "age": user.age,
            "location": list(user.location.all().values_list("name", flat=True))
        })


@method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    fields = ["username", "first_name", "last_name", "role", "age", "password", "location"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        user_data = json.loads(request.body)

        self.object.username = user_data["username"]
        self.object.first_name = user_data["first_name"]
        self.object.last_name = user_data["last_name"]
        self.object.password = user_data["password"]
        self.object.role = user_data["role"]
        self.object.age = user_data["age"]

        for location in user_data["location"]:
            location_obj, created = Location.objects.get_or_create(name=location, defaults={
                "lat": "55",
                "lng": "55"
            })
            self.object.location.add(location_obj)
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "username": self.object.username,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "role": self.object.role,
            "age": self.object.age,
            "location": list(self.object.location.all().values_list("name", flat=True))
        })


@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


class UserAdsDetailView(View):
    def get(self, request):
        user_qs = User.objects.annotate(advertises=Count('ads'))

        paginator = Paginator(user_qs, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        users = []

        for user in page_obj:
            users.append({
                "id": user.id,
                "username": user.username,
                "advertises": user.advertises
            })
        response = {
            "items": users,
            "total": paginator.count,
            "num_pages": paginator.num_pages,
            "avg": user_qs.aggregate(avg=Avg('advertises'))["avg"]
        }

        return JsonResponse(response)