from rest_framework import serializers

from .models import (
    City, Country, Language,
    Skill
)


class CitySerializer(serializers.ModelSerializer):
    """
    CitySerializer is a serializer class that serializes City model instances to JSON format. It uses the
    ModelSerializer subclass from the Django REST Framework to automatically generate serializer fields for the City
    model fields.

    Attributes:
        model (Model): The City model that the serializer is based on.
        fields (tuple): The fields to be serialized in the City model.

    """
    class Meta:
        model = City
        fields = (
            'id',
            'title',
        )


class CountrySerializer(serializers.ModelSerializer):
    """
    CountrySerializer is a serializer class that serializes Country model instances to JSON format. It uses the
    ModelSerializer subclass from the Django REST Framework to automatically generate serializer fields for the Country
    model fields.

    Attributes:
        model (Model): The Country model that the serializer is based on.
        fields (tuple): The fields to be serialized in the Country model.

    """
    class Meta:
        model = Country
        fields = (
            'id',
            'title',
        )


class LanguageSerializer(serializers.ModelSerializer):
    """
    LanguageSerializer is a serializer class that serializes Language model instances to JSON format. It uses the
    ModelSerializer subclass from the Django REST Framework to automatically generate serializer fields for the Language
    model fields.

    Attributes:
        model (Model): The Language model that the serializer is based on.
        fields (tuple): The fields to be serialized in the Language model.

    """
    class Meta:
        model = Language
        fields = (
            'id',
            'title',
        )


class SkillSerializer(serializers.ModelSerializer):
    """
    SkillSerializer is a serializer class that serializes Skill model instances to JSON format. It uses the
    ModelSerializer subclass from the Django REST Framework to automatically generate serializer fields for the Skill
    model fields.

    Attributes:
        model (Model): The Skill model that the serializer is based on.
        fields (tuple): The fields to be serialized in the Skill model.

    """
    class Meta:
        model = Skill
        fields = (
            'id',
            'title',
        )
