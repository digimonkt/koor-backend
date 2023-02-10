from rest_framework import serializers

from project_meta.models import (
    Country
)


class CountrySerializers(serializers.ModelSerializer):
    """
    Serializer class for the `Country` model.

    The `CountrySerializers` class extends `serializers.ModelSerializer`
    and is used to create instances of the `Country` model. It defines the fields
    that should be included in the serialized representation of the model, including
    'title', 'currency_code', 'country_code', 'iso_code2', and 'iso_code3'.
    """
    class Meta:
        model = Country
        fields = ['id', 'title', 'currency_code', 'country_code', 'iso_code2', 'iso_code3']
