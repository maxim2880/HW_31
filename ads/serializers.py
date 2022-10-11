from rest_framework import serializers

from ads.models import User, Location, Ads


# Сериализаторы для объявлений

class AdsListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="username"
    )

    category = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = Ads
        fields = '__all__'


# Сериализаторы для пользователей
class UserListSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = User
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = User
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field="name"
    )

    class Meta:
        model = User
        fields = "__all__"

    def is_valid(self, *, raise_exception=False):
        self._location = self.initial_data.pop("location")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        for location in self._location:
            location_obj, _ = Location.objects.get_or_create(name=location)
            user.location.add(location_obj)

        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    password = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = '__all__'

    location = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field="name"
    )

    class Meta:
        model = User
        fields = "__all__"

    def is_valid(self, *, raise_exception=False):
        self._location = self.initial_data.pop("location")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        for location in self._location:
            location_obj, _ = Location.objects.get_or_create(name=location)
            user.location.add(location_obj)

        user.save()
        return user


class UserDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id"]


# Сериализаторы для локаций

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

# class LocationListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Location
#         fields = '__all__'
#
#
# class LocationDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Location
#         fields = '__all__'
#
#
# class LocationCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Location
#         fields = "__all__"
#
#     # def is_valid(self, *, raise_exception=False):
#     #     self._location = self.initial_data.pop("location")
#     #     return super().is_valid(raise_exception=raise_exception)
#     #
#     # def create(self, validated_data):
#     #     user = User.objects.create(**validated_data)
#     #
#     #     for location in self._location:
#     #         location_obj, _ = Location.objects.get_or_create(name=location)
#     #         user.location.add(location_obj)
#     #
#     #     user.save()
#     #     return user
#
#
# class LocationUpdateSerializer(serializers.ModelSerializer):
#     # location = serializers.SlugRelatedField(
#     #     many=True,
#     #     read_only=True,
#     #     slug_field="name"
#     # )
#     #
#     # password = serializers.CharField(read_only=True)
#
#     class Meta:
#         model = Location
#         fields = '__all__'
#
#     # location = serializers.SlugRelatedField(
#     #     required=False,
#     #     many=True,
#     #     queryset=Location.objects.all(),
#     #     slug_field="name"
#     # )
#     #
#     # class Meta:
#     #     model = User
#     #     fields = "__all__"
#     #
#     # def is_valid(self, *, raise_exception=False):
#     #     self._location = self.initial_data.pop("location")
#     #     return super().is_valid(raise_exception=raise_exception)
#     #
#     # def create(self, validated_data):
#     #     user = User.objects.create(**validated_data)
#     #
#     #     for location in self._location:
#     #         location_obj, _ = Location.objects.get_or_create(name=location)
#     #         user.location.add(location_obj)
#     #
#     #     user.save()
#     #     return user
#
#
# class LocationDestroySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Location
#         fields = ["id"]
