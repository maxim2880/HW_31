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
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.models import Categories, Ad, Selection
from ads.permissions import IsOwnerAdOrStaff, IsOwnerSelection
from users.models import User
from users.serializers import UserDetailSerializer, UserListSerializer, UserCreateSerializer, UserUpdateSerializer, \
    UserDestroySerializer, LocationSerializer
from ads.serializers import AdsListSerializer, AdsDetailSerializer, SelectionListSerializer, SelectionDetailSerializer, \
    SelectionCreateSerializer, AdsUpdateSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
    queryset = Ad.objects.order_by("-price").all()
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


# class AdsDetailView(DetailView):
#     model = Ad
#
#     def get(self, request, *args, **kwargs):
#         advertise = self.get_object()
#
#         return JsonResponse({
#             "id": advertise.id,
#             "name": advertise.name,
#             "author": advertise.author_id,
#             "price": advertise.price,
#             "description": advertise.description,
#             "is_published": advertise.is_published,
#             "image": advertise.image.url if advertise.image else None,
#             "category": advertise.category_id
#         })

@method_decorator(csrf_exempt, name="dispatch")
class AdsCreateView(CreateView):
    model = Ad
    fields = ["name", "author", "price", "description", "is_published", "image", "category"]

    def post(self, request, *args, **kwargs):
        adv_data = json.loads(request.body)
        advertise = Ad.objects.create(
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


class AdsUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerAdOrStaff]
    serializer_class = AdsUpdateSerializer


class AdsDeleteView(DestroyAPIView):
    queryset = Ad.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerAdOrStaff]
    serializer_class = AdsUpdateSerializer


# Работа с картинками

@method_decorator(csrf_exempt, name="dispatch")
class AdsImageView(UpdateView):
    model = Ad
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


class AdsDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdsDetailSerializer
    permission_classes = [IsAuthenticated]


# Вьюхи для подборок

class SelectionListView(ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionListSerializer


class SelectionDetailView(RetrieveAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDetailSerializer


class SelectionCreateView(CreateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateSerializer
    permission_classes = [IsAuthenticated]


class SelectionUpdateView(UpdateAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateSerializer
    permission_classes = [IsAuthenticated, IsOwnerSelection]


class SelectionDeleteView(DestroyAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionCreateSerializer
    permission_classes = [IsAuthenticated]
