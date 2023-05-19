from datetime import date

from django.db.models import Q
from rest_framework import serializers

from jobs.models import (
    JobCategory, JobDetails,
    JobSubCategory
)
from project_meta.models import (
    Country, City, EducationLevel,
    Language, Skill, Tag,
    AllCountry, Choice, OpportunityType
)
from project_meta.serializers import (
    CitySerializer, CountrySerializer,
    TagSerializer, ChoiceSerializer,
    OpportunityTypeSerializer
)

from tenders.models import TenderCategory, TenderDetails
from tenders.serializers import TenderCategorySerializer

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
        read_only_fields = ['id']    


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
    country_name = serializers.CharField(
            style={"input_type": "text"},
            write_only=True,
            allow_blank=False
        )
    class Meta:
        model = City
        fields = ['id', 'title', 'country_name']
        read_only_fields = ['id'] 

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
        country_name = data.get("country_name")
        title = data.get("title")
        if country_name in ["", None]:
            raise serializers.ValidationError({'country_name': 'Country name can not be blank'})
        else:
            try:
                country_instance = Country.objects.get(title=country_name)
                if City.objects.filter(title__iexact=title, country=country_instance).exists():
                    raise serializers.ValidationError({'title': title + ' in ' + str(country_instance.title) + ' already exist.'})
                return data
            except Country.DoesNotExist:
                raise serializers.ValidationError('Country not available.', code='country_name')

    def save(self):
        country_instance = Country.objects.get(title=self.validated_data['country_name'])
        city_instance = City.objects.create(title=self.validated_data['title'], country=country_instance)
        return city_instance

class GetCitySerializers(serializers.ModelSerializer):
    """
    Serializer class for the `City` model.

    The `GetCitySerializers` class extends `serializers.ModelSerializer` and is used to create instances of the
    `City` model. It defines the fields that should be included in the serialized representation of the model,
    including 'id', 'title', 'country'.
    """
    country = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ['id', 'title', 'country']
        read_only_fields = ['id'] 

    def get_country(self, obj):
        return {"id": obj.country.id, "title": obj.country.title}


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
        read_only_fields = ['id'] 

    def validate(self, data):
        """
        Validate the data before saving to the database.
        
        The validate method checks if the category field is blank and raises a validation error if it is.
        It also checks if a job sub category with the same title and category already exists and raises a validation error if it
        does.
        Finally, it checks if the category exists in the database and raises a validation error if it does not.

        Args:
            data (dict): Dictionary of data to be validated.

        Raises:
            serializers.ValidationError: Raised if the category field is blank or if a job sub category with the same title and
            category already exists or if the category does not exist in the database.

        Returns:
            data (dict): The validated data.
        """
        title = data.get("title")
        if JobCategory.objects.filter(title__iexact=title, is_removed=False).exists():
            raise serializers.ValidationError({'title': title + ' already exist.'})
        return data

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        return instance


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
        read_only_fields = ['id'] 

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        return instance


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
        read_only_fields = ['id'] 

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        return instance


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
        read_only_fields = ['id'] 

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        return instance


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
        read_only_fields = ['id'] 

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        return instance


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
        read_only_fields = ['id'] 


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
        read_only_fields = ['id'] 

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
        read_only_fields = ['id'] 

    def validate(self, data):
        title = data.get("title")
        if TenderCategory.objects.filter(title=title).exists():
            raise serializers.ValidationError({'title': str(title) + ' already exists'})
        else:
            return data
    
    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        return instance


class GetJobSubCategorySerializers(serializers.ModelSerializer):
    """
    Serializer class for the `JobSubCategory` model.

    The `GetJobSubCategorySerializers` class extends `serializers.ModelSerializer` and is used to create instances of the
    `JobSubCategory` model. It defines the fields that should be included in the serialized representation of the model,
    including 'id', 'title', 'category'.
    """
    category = serializers.SerializerMethodField()

    class Meta:
        model = JobSubCategory
        fields = ['id', 'title', 'category']
        read_only_fields = ['id'] 

    def get_category(self, obj):
        return {"id": obj.category.id, "title": obj.category.title}


class JobSubCategorySerializers(serializers.ModelSerializer):
    """
    Serializer class for the `JobSubCategory` model.

    The `JobSubCategorySerializers` class extends `serializers.ModelSerializer` and is used to create instances of the
    `JobSubCategory` model. It defines the fields that should be included in the serialized representation of the model,
    including 'id', 'title', 'category'.
    """

    class Meta:
        model = JobSubCategory
        fields = ['id', 'title', 'category']
        read_only_fields = ['id'] 

    def validate(self, data):
        """
        Validate the data before saving to the database.
        
        The validate method checks if the category field is blank and raises a validation error if it is.
        It also checks if a job sub category with the same title and category already exists and raises a validation error if it
        does.
        Finally, it checks if the category exists in the database and raises a validation error if it does not.

        Args:
            data (dict): Dictionary of data to be validated.

        Raises:
            serializers.ValidationError: Raised if the category field is blank or if a job sub category with the same title and
            category already exists or if the category does not exist in the database.

        Returns:
            data (dict): The validated data.
        """
        category = data.get("category")
        title = data.get("title")
        if category in ["", None]:
            raise serializers.ValidationError({'category': 'category can not be blank'})
        else:
            try:
                if JobCategory.objects.get(title=category.title):
                    if JobSubCategory.objects.filter(title__iexact=title, category=category).exists():
                        raise serializers.ValidationError(
                            {'title': title + ' in ' + category.title + ' already exist.'})
                    return data
            except JobCategory.DoesNotExist:
                raise serializers.ValidationError('Job category not available.', code='category')

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        return instance


class AllCountrySerializers(serializers.ModelSerializer):
    """
    Serializer class for the `AllCountry` model.

    The `AllCountrySerializers` class extends `serializers.ModelSerializer` and is used to create instances of the
    `AllCountry` model. It defines the fields that should be included in the serialized representation of the model,
    including 'id', 'title', 'currency', 'phone_code', 'iso_code2', and 'iso_code3'.
    """

    class Meta:
        model = AllCountry
        fields = ['id', 'title', 'currency', 'phone_code', 'iso2', 'iso3']
        read_only_fields = ['id'] 


class AllCitySerializers(serializers.ModelSerializer):
    """
    Serializer for AllCity model that returns a serialized representation of each city, including its
    country information. The 'country' field is a custom serializer method that returns the country information
     as a dictionary with 'id' and 'title' keys.

    Attributes:
        - `country`: A custom `SerializerMethodField` that returns the serialized representation of the country
                    foreign key field of AllCity model.

    Meta:
        - `model`: AllCity model for which the serializer is defined.
        - `fields`: A list of fields to be included in the serialized representation of the AllCity model.
                    It includes 'id', 'title', and 'country' fields.

    """

    country = serializers.SerializerMethodField()

    class Meta:
        model = AllCountry
        fields = ['id', 'title', 'country']
        read_only_fields = ['id'] 

    def get_country(self, obj):
        return {"id": obj.country.id, "title": obj.country.title}


class ChoiceSerializers(serializers.ModelSerializer):
    """
    Serializer class for the `Choice` model.

    The `ChoiceSerializers` class extends `serializers.ModelSerializer` and is used to create instances of the
    `Choice` model. It defines the fields that should be included in the serialized representation of the model,
    including 'id', 'title'.
    """

    class Meta:
        model = Choice
        fields = ['id', 'title']
        read_only_fields = ['id'] 

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        return instance


class OpportunityTypeSerializers(serializers.ModelSerializer):
    """
    Serializer class for the `OpportunityType` model.

    The `OpportunityTypeSerializers` class extends `serializers.ModelSerializer` and is used to create instances of the
    `OpportunityType` model. It defines the fields that should be included in the serialized representation of the model,
    including 'id', 'title'.
    """

    class Meta:
        model = OpportunityType
        fields = ['id', 'title']
        read_only_fields = ['id'] 

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        return instance


class TenderListSerializers(serializers.ModelSerializer):
    """
    `TenderListSerializers` class is a Django REST Framework serializer used for serializing TenderDetails model data
    into JSON format with selected fields.

    Attributes:
        - `country (serializers.SerializerMethodField)`: SerializerMethodField used for serializing country field of
            `TenderDetails` model
        - `city (serializers.SerializerMethodField)`: SerializerMethodField used for serializing city field of
            `TenderDetails` model
        - `Meta (class): Class used for defining metadata options for the serializer
            - `model (class)`: Model class to be serialized
            - `fields (list)`: List of fields to be included in the serialized output

    Example usage:
        To serialize TenderDetails model data into JSON format with selected fields:
        - `serializer` = `TenderListSerializers`(queryset, many=True)
        - `serialized_data` = `serializer.data`
    """
    country = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    tag = serializers.SerializerMethodField()
    tender_category = serializers.SerializerMethodField()
    tender_type = serializers.SerializerMethodField()
    sector = serializers.SerializerMethodField()

    class Meta:
        model = TenderDetails
        fields = [
            'id', 'tender_id', 'title', 'tag', 'tender_category', 
            'tender_type', 'sector', 'city', 'country', 'status', 'user'
            ]
        read_only_fields = ['id'] 

    def get_country(self, obj):
        """
        Retrieves the serialized data for the country related to a TenderDetails object.

        Args:
            obj: The TenderDetails object to retrieve the country data for.

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
        Retrieves the serialized data for the city related to a TenderDetails object.

        Args:
            obj: The TenderDetails object to retrieve the city data for.

        Returns:
            A dictionary containing the serialized city data.

        """

        context = {}
        get_data = CitySerializer(obj.city)
        if get_data.data:
            context = get_data.data
        return context

    def get_tag(self, obj):

        context = []
        get_data = TagSerializer(obj.tag, many=True)
        if get_data.data:
            context = get_data.data
        return context

    def get_tender_category(self, obj):

        context = []
        get_data = TenderCategorySerializer(obj.tender_category, many=True)
        if get_data.data:
            context = get_data.data
        return context

    def get_tender_type(self, obj):

        context = {}
        if obj.sector:
            get_data = OpportunityTypeSerializer(obj.tender_type, many=True)
            if get_data.data:
                context = get_data.data[0]
        return context

    def get_sector(self, obj):

        context = {}
        if obj.sector:
            get_data = ChoiceSerializer(obj.sector, many=True)
            if get_data.data:
                context = get_data.data[0]
        return context

    def get_user(self, obj):
        return obj.user.name
