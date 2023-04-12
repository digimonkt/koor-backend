from datetime import date

from django.db.models import Q
from rest_framework import serializers

from jobs.models import (
    JobCategory, JobDetails
)
from project_meta.models import (
    Country, City, EducationLevel,
    Language, Skill, Tag,
    JobSeekerCategory, Sector
)
from project_meta.serializers import (
    CitySerializer, CountrySerializer
)

from tenders.models import TenderCategory

from users.backends import MobileOrEmailBackend as cb
from users.models import User, UserSession

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
    The `ChangePasswordSerializers` class handles the serialization of data for changing user password.

    Parameters:
        - `old_password (str)`: The old password of the user.
        - `password (str)`: The new password of the user.

    Methods:
        - `validate(data)`: Validates the old password provided by the user and sets the new password if it is valid.

    Returns:
        - `user (User)`: The updated user instance with the new password.

    Raises:
        - `serializers.ValidationError`: If the old password provided is invalid or if any error occurs during the
            validation process.

    """

    old_password = serializers.CharField(
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
        user_data = self.context['user']
        user = None
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


class CandidatesSerializers(serializers.ModelSerializer):
    """
    Serializer class for the `User` model.

    The `CandidatesSerializers` class extends `serializers.ModelSerializer` and is used to create instances of the
    `User` model. It defines the fields that should be included in the serialized representation of the model,
    including 'id', 'role', 'name', 'email', 'country_code', 'mobile_number', 'is_active'.
    """

    class Meta:
        model = User
        fields = ['id', 'role', 'name', 'email', 'country_code', 'mobile_number', 'is_active']


class JobListSerializers(serializers.ModelSerializer):
    """
    `JobListSerializers` class is a Django REST Framework serializer used for serializing JobDetails model data
    into JSON format with selected fields.

    Attributes:
        - `country (serializers.SerializerMethodField)`: SerializerMethodField used for serializing country field of
            `JobDetails` model
        - `city (serializers.SerializerMethodField)`: SerializerMethodField used for serializing city field of
            `JobDetails` model
        - `Meta (class): Class used for defining metadata options for the serializer
            - `model (class)`: Model class to be serialized
            - `fields (list)`: List of fields to be included in the serialized output

    Example usage:
        To serialize JobDetails model data into JSON format with selected fields:
        - `serializer` = `JobListSerializers`(queryset, many=True)
        - `serialized_data` = `serializer.data`
    """
    country = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = JobDetails
        fields = ['id', 'job_id', 'title', 'address', 'city', 'country', 'status', 'user']

    def get_country(self, obj):
        """
        Retrieves the serialized data for the country related to a JobDetails object.

        Args:
            obj: The JobDetails object to retrieve the country data for.

        Returns:
            A dictionary containing the serialized country data.

        """

        context = {}
        get_data = CountrySerializer(obj.country)
        if get_data.data:
            context = get_data.data
        return context

    def get_city(self, obj):
        """
        Retrieves the serialized data for the city related to a JobDetails object.

        Args:
            obj: The JobDetails object to retrieve the city data for.

        Returns:
            A dictionary containing the serialized city data.

        """

        context = {}
        get_data = CitySerializer(obj.city)
        if get_data.data:
            context = get_data.data
        return context

    def get_user(self, obj):
        return obj.user.name


class UserCountSerializers(serializers.Serializer):
    """
    A serializer that converts user count data to/from JSON format.

    Attributes:
        - `total_user (int)`: The total number of registered users in the system.
        - `job_seekers (int)`: The number of registered users with the 'job_seeker' role.
        - `employers (int)`: The number of registered users with the 'employer' role.
        - `vendors (int)`: The number of registered users with the 'vendor' role.
        - `active_user (int)`: The number of users who are currently logged in to the system.
        - `total_jobs (int)`: The total number of jobs posted in the system.
        - `active_jobs (int)`: The number of jobs that are currently active and open for applications.

    Methods:
        - `get_active_jobs(self, obj)`: Retrieves the count of active jobs.
        - `get_total_jobs(self, obj)`: Retrieves the count of total jobs.
        - `get_total_user(self, obj)`: Retrieves the count of total users.
        - `get_active_user(self, obj)`: Retrieves the count of active users.
        - `get_job_seekers(self, obj)`: Retrieves the count of job seekers.
        - `get_employers(self, obj)`: Retrieves the count of employers.
        - `get_vendors(self, obj)`: Retrieves the count of vendors.

    Returns:
        JSON-serializable data: The data containing the count of users and jobs in the system.
    """

    total_user = serializers.SerializerMethodField()
    job_seekers = serializers.SerializerMethodField()
    employers = serializers.SerializerMethodField()
    vendors = serializers.SerializerMethodField()
    active_user = serializers.SerializerMethodField()
    total_jobs = serializers.SerializerMethodField()
    active_jobs = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'total_jobs', 'active_jobs', 'total_user', 'job_seekers',
            'employers', 'vendors', 'active_user'
        ]

    def get_active_jobs(self, obj):
        return JobDetails.objects.filter(status='active', start_date__lte=date.today(),
                                         deadline__gte=date.today()).count()

    def get_total_jobs(self, obj):
        return JobDetails.objects.count()

    def get_total_user(self, obj):
        return User.objects.filter(~Q(role='admin')).count()

    def get_active_user(self, obj):
        return UserSession.objects.filter(~Q(user__role='admin')).filter(expire_at=None).order_by('user').distinct(
            'user').count()

    def get_job_seekers(self, obj):
        return User.objects.filter(role='job_seeker').count()

    def get_employers(self, obj):
        return User.objects.filter(role='employer').count()

    def get_vendors(self, obj):
        return User.objects.filter(role='vendor').count()


class DashboardCountSerializers(serializers.Serializer):
    """
    `DashboardCountSerializers` is a serializer class that takes a User model and returns the count of `active jobs` and
    `employers` within a given `date range`. The class has two serializer method fields, '`employers`' and '`jobs`',
    which retrieve the count of `employers` and `jobs` respectively.

    Attributes:
    - `employers (serializers.SerializerMethodField)`: The method field that retrieves the `count of employers`.
    - `jobs (serializers.SerializerMethodField)`: The method field that retrieves the `count of active jobs`.

    Methods:
    - `get_jobs(obj)`: A method that returns the `count of active jobs` within the `specified date range`.
    - `get_employers(obj)`: A method that returns the `count of employers` within the `specified date range`.

    Example usage:
    - `serializer` = DashboardCountSerializers(context={'start_date': '2022-01-01', 'end_date': '2022-12-31'})
    - `serialized_data` = serializer.data

    """

    employers = serializers.SerializerMethodField()
    jobs = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'employers', 'jobs'
        ]

    def get_jobs(self, obj):
        start_date = self.context['start_date']
        end_date = self.context['end_date']
        return JobDetails.objects.filter(
            start_date__lte=date.today(), deadline__gte=date.today(),
            created__gte=start_date, created__lte=end_date,
            status='active').count()

    def get_employers(self, obj):
        start_date = self.context['start_date']
        end_date = self.context['end_date']
        return User.objects.filter(
            date_joined__gte=start_date, date_joined__lte=end_date,
            role='employer').count()


class JobSeekerCategorySerializers(serializers.ModelSerializer):
    """
    A serializer class for the `JobSeekerCategory` model. It serializes and deserializes data
    to and from JSON format for API calls.

    Attributes:
        - `Meta (class)`: A subclass of ModelSerializer which defines the metadata for the serializer.

    Methods:
        - `validate_category(category)`: Validates the category field in the serialized data.

    """

    class Meta:
        model = JobSeekerCategory
        fields = ['id', 'title', 'category']

    def validate_category(self, category):
        """
        Validates the category field in the serialized data. If the category is not blank and is
        a valid category, returns the category. Otherwise, raises a validation error with an
        appropriate message.

        Args:
            - `category (str)`: The category to be validated.

        Raises:
            - `serializers.ValidationError`: If the category is invalid or blank.

        Returns:
            - `str`: The validated category.

        """

        if category != '':
            try:
                if JobSeekerCategory.objects.get(id=category.id):
                    if JobSeekerCategory.objects.filter(id=category.id, category=None):
                        return category
                    else:
                        raise serializers.ValidationError('This is a sub category.', code='category')
            except JobSeekerCategory.DoesNotExist:
                raise serializers.ValidationError('Invalid category.', code='category')
        else:
            raise serializers.ValidationError('category can not be blank', code='category')


class TenderCategorySerializers(serializers.ModelSerializer):
    """
    Serializer class for the `TenderCategory` model.

    The `TenderCategorySerializers` class extends `serializers.ModelSerializer` and is used to create instances of the
    `TenderCategory` model. It defines the fields that should be included in the serialized representation of the model,
    including 'id', 'title'.
    """

    class Meta:
        model = TenderCategory
        fields = ['id', 'title']


class SectorSerializers(serializers.ModelSerializer):
    """
    Serializer class for the `Sector` model.

    The `SectorSerializers` class extends `serializers.ModelSerializer` and is used to create instances of the
    `Sector` model. It defines the fields that should be included in the serialized representation of the model,
    including 'id', 'title'.
    """

    class Meta:
        model = Sector
        fields = ['id', 'title']
