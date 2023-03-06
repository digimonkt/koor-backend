from rest_framework import serializers

from jobs.models import (
    JobCategory
)
from project_meta.models import (
    Country, City, EducationLevel,
    Language, Skill, Tag
)

from users.backends import MobileOrEmailBackend as cb

from .models import Content


class CountrySerializers(serializers.ModelSerializer):
    """
    Serializer class for the `Country` model.

    The `CountrySerializers` class extends `serializers.ModelSerializer` and is used to create instances of the
    `Country` model. It defines the fields that should be included in the serialized representation of the model,
    including 'id', 'title', 'currency_code', 'country_code', 'iso_code2', and 'iso_code3'.
    """

    class Meta:
        model = Country
        fields = ['id', 'title', 'currency_code', 'country_code', 'iso_code2', 'iso_code3']


class CitySerializers(serializers.ModelSerializer):
    """
    Serializer class for City model.
    
    - This serializer class is based on Django Rest Framework's ModelSerializer, and it is used to represent the City
    model in the API.
    - The serializer defines the fields that should be included in the API representation using the fields attribute.
    - The serializer also includes a validation method (validate) to validate the data before it is saved to the
    database.
    - The validate method checks if the country field is blank and raises a validation error if it is.
    - It also checks if a city with the same title and country already exists and raises a validation error if it does.
    - Finally, it checks if the country exists in the database and raises a validation error if it does not.

    Attributes:
        - model (City): The model class that this serializer is based on.
        - fields (list): List of fields from the City model that should be included in the API representation.
    """

    class Meta:
        model = City
        fields = ['id', 'title', 'country']

    def validate(self, data):
        """
        Validate the data before saving to the database.
        
        The validate method checks if the country field is blank and raises a validation error if it is.
        It also checks if a city with the same title and country already exists and raises a validation error if it
        does.
        Finally, it checks if the country exists in the database and raises a validation error if it does not.

        Args:
            data (dict): Dictionary of data to be validated.

        Raises:
            serializers.ValidationError: Raised if the country field is blank or if a city with the same title and
            country already exists or if the country does not exist in the database.

        Returns:
            data (dict): The validated data.
        """
        country = data.get("country")
        title = data.get("title")
        if country in ["", None]:
            raise serializers.ValidationError({'country': 'Country can not be blank'})
        else:
            try:
                if Country.objects.get(title=country.title):
                    if City.objects.filter(title=title, country=country).exists():
                        raise serializers.ValidationError({'title': title + ' in ' + country.title + ' already exist.'})
                    return data
            except Country.DoesNotExist:
                raise serializers.ValidationError('Country not available.', code='country')


class JobCategorySerializers(serializers.ModelSerializer):
    """
    Serializer class for the `JobCategory` model.

    The `JobCategorySerializers` class extends `serializers.ModelSerializer` and is used to create instances of the
    `JobCategory` model. It defines the fields that should be included in the serialized representation of the model,
    including 'id', 'title'.
    """

    class Meta:
        model = JobCategory
        fields = ['id', 'title']


class EducationLevelSerializers(serializers.ModelSerializer):
    """
    Serializer class for the `EducationLevel` model.

    The `EducationLevelSerializers` class extends `serializers.ModelSerializer` and is used to create instances of the
    `EducationLevel` model. It defines the fields that should be included in the serialized representation of the model,
    including 'id', 'title'.
    """

    class Meta:
        model = EducationLevel
        fields = ['id', 'title']


class LanguageSerializers(serializers.ModelSerializer):
    """
    Serializer class for the ` Language` model.

    The `LanguageSerializers` class extends `serializers.ModelSerializer` and is used to create instances of the
    `Language` model. It defines the fields that should be included in the serialized representation of the model,
    including 'id', 'title'.
    """

    class Meta:
        model = Language
        fields = ['id', 'title']


class SkillSerializers(serializers.ModelSerializer):
    """
    Serializer class for the ` Skill` model.

    The `SkillSerializers` class extends `serializers.ModelSerializer` and is used to create instances of the
    `Skill` model. It defines the fields that should be included in the serialized representation of the model,
    including 'id', 'title'.
    """

    class Meta:
        model = Skill
        fields = ['id', 'title']


class TagSerializers(serializers.ModelSerializer):
    """
    Serializer class for the `Tag` model.

    The `TagSerializers` class extends `serializers.ModelSerializer` and is used to create instances of the
    `Tag` model. It defines the fields that should be included in the serialized representation of the model,
    including 'id', 'title'.
    """

    class Meta:
        model = Tag
        fields = ['id', 'title']


class ChangePasswordSerializers(serializers.Serializer):
    """
    A serializer class to validate the request data for changing user password.

    `Attributes`:
        - `old_password (serializers.CharField)`: A field to receive the old password from the request.
        - `confirm_password (serializers.CharField)`: A field to receive the confirmation password from the request.
        - `password (serializers.CharField)`: A field to receive the new password from the request.

    `Methods`:
        - `validate(data)`: A method to validate the request data. It receives a dictionary of request data and returns
        a validated user object or raises a validation error. It compares the new password and confirm password fields,
        authenticates the user using the old password, and updates the password if the authentication is successful.

    `Raises`:
        - `serializers.ValidationError`: If the request data is invalid or if the authentication fails.

    `Returns`:
        - A validated user object after successful authentication and password update, or raises a validation error if
        the request data is invalid or if the authentication fails.

    """

    old_password = serializers.CharField(
        style={"input_type": "text"},
        write_only=True
    )
    confirm_password = serializers.CharField(
        style={"input_type": "text"},
        write_only=True
    )
    password = serializers.CharField(
        style={"input_type": "text"},
        write_only=True
    )

    def validate(self, data):
        old_password = data.get("old_password", "")
        password = data.get("password", "")
        confirm_password = data.get("confirm_password", "")
        user_data = self.context['user']
        user = None
        if password != confirm_password:
            raise serializers.ValidationError({'password': 'Confirm password not match.'})
        try:
            user = cb.authenticate(self, identifier=user_data.email, password=old_password, role="admin")
            if user:
                user.set_password(password)
                user.save()
                return user
            else:
                raise serializers.ValidationError({'message': 'Invalid login credentials.'})
        except:
            raise serializers.ValidationError({'message': 'Invalid login credentials.'})


class ContentSerializers(serializers.ModelSerializer):
    """
    Serializer class for the `Content` model.

    The `ContentSerializers` class extends `serializers.ModelSerializer` and is used to create instances of the
    `Content` model. It defines the fields that should be included in the serialized representation of the model,
    including 'description'.
    """

    class Meta:
        model = Content
        fields = ['description']
        
    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        return instance
