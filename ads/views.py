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
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from ads.models import Categories, Ads, User, Location
from ads.serializers import UserDetailSerializer, UserListSerializer, UserCreateSerializer, UserUpdateSerializer, \
    UserDestroySerializer, LocationSerializer, AdsListSerializer


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

class AdsListView(ListAPIView):
    queryset = Ads.objects.order_by("-price").all()
    serializer_class = AdsListSerializer

    def get(self, request, *args, **kwargs):
        categories = request.GET.getlist('cat', [])
        if categories:
            self.queryset = self.queryset.filter(category_id__in=categories)
        text = request.GET.get('text')
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)
        location = request.GET.get('location')
        if location:
            self.queryset = self.queryset.filter(author__location__name__icontains=location)
        price_from = request.GET.get('price_from')
        price_to = request.GET.get('price_to')
        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)
        return super().get(self, *args, **kwargs)


    # model = Ads
    #
    # def get(self, request, *args, **kwargs):
    #     super().get(request, *args, **kwargs)
    #
    #     # Пагинация
    #
    #     paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
    #     page_number = request.GET.get("page")
    #     page_obj = paginator.get_page(page_number)
    #
    #     self.object_list = self.object_list.select_related("user").order_by("-price")
    #
    #     advertises = []
    #     for advertise in page_obj:
    #         advertises.append({
    #             "id": advertise.id,
    #             "name": advertise.name,
    #             "author": advertise.author_id,
    #             "price": advertise.price,
    #             "description": advertise.description,
    #             "is_published": advertise.is_published,
    #             "image": advertise.image.url,
    #             "category": advertise.category_id
    #         })
    #     response = {
    #         "items": advertises,
    #         "num_pages": paginator.num_pages,
    #         "total": paginator.count
    #     }
    #     return JsonResponse(response, safe=False, status=200)


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


# Предстваления для пользователей

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDestroySerializer


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


# Представления и ViewSet для локаций

class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

# class LocationListView(ListAPIView):
#     queryset = Location.objects.all()
#     serializer_class = LocationListSerializer
#
#
# class LocationDetailView(RetrieveAPIView):
#     queryset = Location.objects.all()
#     serializer_class = LocationDetailSerializer
#
#
# class LocationCreateView(CreateAPIView):
#     queryset = Location.objects.all()
#     serializer_class = LocationCreateSerializer
#
#
# class LocationUpdateView(UpdateAPIView):
#     queryset = Location.objects.all()
#     serializer_class = LocationUpdateSerializer
#
#
# class LocationDeleteView(DestroyAPIView):
#     queryset = Location.objects.all()
#     serializer_class = LocationDestroySerializer
