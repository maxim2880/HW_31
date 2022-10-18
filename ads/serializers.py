from rest_framework import serializers

from ads.models import Ad, Categories, Selection
from users.models import User


class AdsListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    category = serializers.SlugRelatedField(slug_field="name", queryset=User.objects.all())

    class Meta:
        model = Ad
        exclude = ['id']


class AdsDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    category = serializers.SlugRelatedField(slug_field="name", queryset=User.objects.all())

    class Meta:
        model = Ad
        fields = '__all__'

class AdsUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ad
        fields = '__all__'


class SelectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'


class SelectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ['id', 'name']


class SelectionDetailSerializer(serializers.ModelSerializer):
    items = AdsListSerializer(many=True)

    class Meta:
        model = Selection
        fields = '__all__'
