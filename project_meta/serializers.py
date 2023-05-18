from rest_framework import serializers

from .models import (
    City, Country, Language,
    Skill, EducationLevel, Tag,
    Choice, OpportunityType
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


class HighestEducationSerializer(serializers.ModelSerializer):
    """
    HighestEducationSerializer is a serializer class that serializes EducationLevel model instances to JSON format. It uses the
    ModelSerializer subclass from the Django REST Framework to automatically generate serializer fields for the EducationLevel
    model fields.

    Attributes:
        model (Model): The EducationLevel model that the serializer is based on.
        fields (tuple): The fields to be serialized in the EducationLevel model.

    """
    class Meta:
        model = EducationLevel
        fields = (
            'id',
            'title',
        )


class TagSerializer(serializers.ModelSerializer):
    """
    TagSerializer is a serializer class that serializes Tag model instances to JSON format. It uses the
    ModelSerializer subclass from the Django REST Framework to automatically generate serializer fields for the Tag
    model fields.

    Attributes:
        model (Model): The EducationLevel model that the serializer is based on.
        fields (tuple): The fields to be serialized in the Tag model.

    """
    class Meta:
        model = Tag
        fields = (
            'id',
            'title',
        )

class ChoiceSerializer(serializers.ModelSerializer):
    """
    ChoiceSerializer is a serializer class that serializes Choice model instances to JSON format. It uses the
    ModelSerializer subclass from the Django REST Framework to automatically generate serializer fields for the Choice
    model fields.

    Attributes:
        model (Model): The EducationLevel model that the serializer is based on.
        fields (tuple): The fields to be serialized in the Choice model.

    """
    class Meta:
        model = Choice
        fields = (
            'id',
            'title',
        )


class OpportunityTypeSerializer(serializers.ModelSerializer):
    """
    OpportunityTypeSerializer is a serializer class that serializes OpportunityType model instances to JSON format. It uses the
    ModelSerializer subclass from the Django REST Framework to automatically generate serializer fields for the OpportunityType
    model fields.

    Attributes:
        model (Model): The EducationLevel model that the serializer is based on.
        fields (tuple): The fields to be serialized in the OpportunityType model.

    """
    class Meta:
        model = OpportunityType
        fields = (
            'id',
            'title',
        )
