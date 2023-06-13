from datetime import date

from django.db.models import Q
from rest_framework import serializers
from django.template.defaultfilters import slugify

from jobs.models import (
    JobCategory, JobDetails,
    JobSubCategory
)
from project_meta.models import (
    Country, City, EducationLevel,
    Language, Skill, Tag, Media,
    AllCountry, Choice, OpportunityType
)
from project_meta.serializers import (
    CitySerializer, CountrySerializer,
    TagSerializer, ChoiceSerializer,
    OpportunityTypeSerializer
)
from chat.serializers import AttachmentSerializer

from tenders.models import TenderCategory, TenderDetails
from tenders.serializers import TenderCategorySerializer

from users.backends import MobileOrEmailBackend as cb
from users.models import User, UserSession

from .models import (
    Content, ResourcesContent, SocialUrl,
    AboutUs, FaqCategory, FAQ,
    CategoryLogo, Testimonial, NewsletterUser
)


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
        job_category_instance = super().update(instance, validated_data)
        instance.slug = slugify(job_category_instance.title)
        instance.save()
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
        education_instance = super().update(instance, validated_data)
        instance.slug = slugify(education_instance.title)
        instance.save()
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
        language_instance = super().update(instance, validated_data)
        instance.slug = slugify(language_instance.title)
        instance.save()
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
        skill_instance = super().update(instance, validated_data)
        instance.slug = slugify(skill_instance.title)
        instance.save()
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
        tag_instance = super().update(instance, validated_data)
        instance.slug = slugify(tag_instance.title)
        instance.save()
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
        content_instance = super().update(instance, validated_data)
        instance.slug = slugify(content_instance.title)
        instance.save()
        return instance


class CandidatesSerializers(serializers.ModelSerializer):
    """
    Serializer class for the `User` model.

    The `CandidatesSerializers` class extends `serializers.ModelSerializer` and is used to create instances of the
    `User` model. It defines the fields that should be included in the serialized representation of the model,
    including 'id', 'role', 'name', 'email', 'country_code', 'mobile_number', 'is_active'.
    """
    verify = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'role', 'name', 'email', 'country_code', 'mobile_number', 'is_active', 'verify']
        read_only_fields = ['id'] 
    
    def get_verify(self, obj):
        verify = False
        if obj.user_profile_employerprofile_user.first():
            verify = obj.user_profile_employerprofile_user.first().is_verified
        return verify


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
        tender_category_instance = super().update(instance, validated_data)
        instance.slug = slugify(tender_category_instance.title)
        instance.save()
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
        job_sub_category_instance = super().update(instance, validated_data)
        instance.slug = slugify(job_sub_category_instance.title)
        instance.save()
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
        choice_instance = super().update(instance, validated_data)
        instance.slug = slugify(choice_instance.title)
        instance.save()
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
        opportunity_instance = super().update(instance, validated_data)
        instance.slug = slugify(opportunity_instance.title)
        instance.save()
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
            'tender_type', 'sector', 'city', 'country', 'status', 'user', 'address'
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


class CreateResourcesSerializers(serializers.ModelSerializer):
    """
    Serializer class for the `ResourcesContent` model.

    The `CreateResourcesSerializers` class extends `serializers.ModelSerializer` and is used to create instances of the
    `ResourcesContent` model. It defines the fields that should be included in the serialized representation of the model,
    including 'id', 'title', 'category'.
    """
    attachment_file = serializers.FileField(
        style={"input_type": "file"},
        write_only=True,
        allow_null=False
    )
    class Meta:
        model = ResourcesContent
        fields = ['id', 'title', 'description', 'attachment_file']
        read_only_fields = ['id'] 
    
    def save(self):
        attachment_file = None
        if 'attachment_file' in self.validated_data:
            attachment_file = self.validated_data.pop('attachment_file')
        resource_instance = super().save()
        if attachment_file:
            content_type = str(attachment_file.content_type).split("/")
            if content_type[0] not in ["video", "image"]:
                media_type = 'document'
            else:
                media_type = content_type[0]
            # save media file into media table and get instance of saved data.
            media_instance = Media(title=attachment_file.name, file_path=attachment_file, media_type=media_type)
            media_instance.save()
            # save media instance into license id file into employer profile table.
            resource_instance.attachment = media_instance
            resource_instance.save()
        return resource_instance

    def update(self, instance, validated_data):
        attachment_file = None
        if 'attachment_file' in self.validated_data:
            attachment_file = self.validated_data.pop('attachment_file')
        super().update(instance, validated_data)
        if attachment_file:
            content_type = str(attachment_file.content_type).split("/")
            if content_type[0] not in ["video", "image"]:
                media_type = 'document'
            else:
                media_type = content_type[0]
            # save media file into media table and get instance of saved data.
            media_instance = Media(title=attachment_file.name, file_path=attachment_file, media_type=media_type)
            media_instance.save()
            # save media instance into license id file into employer profile table.
            instance.attachment = media_instance
            instance.save()
        return instance


class ResourcesSerializers(serializers.ModelSerializer):
    """
    Serializer for the ResourcesContent model.

    This serializer is used to serialize/deserialize ResourcesContent objects to/from JSON format. It defines
    the fields that will be included in the serialized data and provides validation for deserialization.

    Attributes:
        Meta: A subclass of the serializer that specifies the model to be serialized and the fields
            to be included in the serialized data.
    """
    attachment = serializers.SerializerMethodField()
    class Meta:
        model = ResourcesContent
        fields = (
            'id', 'title', 'description', 'attachment'
        )
    
    def get_attachment(self, obj):
        if obj.attachment:
            return {'id': obj.attachment.id, 
                    'title': obj.attachment.title, 
                    'type':obj.attachment.media_type,
                    'path': obj.attachment.file_path.url
            }
        return None


class SocialUrlSerializers(serializers.ModelSerializer):
    """
    Serializer class for SocialUrl model.

    Serializes the SocialUrl model into JSON format with the specified fields.

    Attributes:
        - model (class): The model class to be serialized (SocialUrl).
        - fields (tuple): The fields to be included in the serialized output (id, platform, url).

    """

    class Meta:
        model = SocialUrl
        fields = (
            'id', 'platform', 'url'
        )
        read_only_fields = ['id'] 


class AboutUsSerializers(serializers.ModelSerializer):
    """
    Serializer for the AboutUs model.

    Serializes the 'id', 'description', and 'image' fields of the AboutUs model.
    The 'image' field is serialized using a custom SerializerMethodField that
    retrieves additional information about the image if it exists.

    Methods:
    - get_image(obj): Retrieves additional information about the image if it exists.

    Attributes:
    - model: The AboutUs model used for serialization.
    - fields: The fields to be serialized from the AboutUs model.

    """
    
    image = serializers.SerializerMethodField()
    class Meta:
        model = AboutUs
        fields = ['id', 'description', 'image']
    
    def get_image(self, obj):
        """
        Retrieves additional information about the image if it exists.

        Parameters:
        - obj: The AboutUs model instance.

        Returns:
        - context: A dictionary containing information about the image.
                   - 'title': The title of the image.
                   - 'path': The path or URL of the image file.
                   - 'type': The media type of the image.
        
        """
        
        context = {}
        if obj.image:
            context['title'] = obj.image.title
            if obj.image.title == "profile image":
                context['path'] = str(obj.image.file_path)
            else:
                context['path'] = obj.image.file_path.url
            context['type'] = obj.image.media_type
            return context
        return None
        

class UpdateAboutUsSerializers(serializers.ModelSerializer):
    """
    Serializer for updating About Us data.

    Fields:
    - description: A string representing the description of About Us.
    - image_file: A file field representing the image file for About Us.

    Methods:
    - validate_image_file: Validates the image file and ensures it is not blank and has a valid format.
    - update: Updates the instance of AboutUs model with the validated data, including saving the image file as media.

    """
    
    image_file = serializers.FileField(
        style={"input_type": "file"},
        write_only=True,
        allow_null=False
    )
    class Meta:
        model = AboutUs
        fields = ['description', 'image_file']
        
    
    def validate_image_file(self, image_file):
        """
        Validates the image file and ensures it is not blank and has a valid format.

        Parameters:
        - image_file: The image file to be validated.

        Returns:
        - The validated image file if it passes the validation.

        Raises:
        - serializers.ValidationError: If the image file is blank or has an invalid format.

        """
        
        if image_file in ["", None]:
            raise serializers.ValidationError('Image file can not be blank.', code='image_file')
        content_type = str(image_file.content_type).split("/")
        if content_type[0] == "image":
            return image_file
        else:
            raise serializers.ValidationError('Invalid image file.', code='image_file')

    def update(self, instance, validated_data):
        """
        Updates the instance of AboutUs model with the validated data, including saving the image file as media.

        Parameters:
        - instance: The instance of AboutUs model to be updated.
        - validated_data: The validated data for updating the instance.

        Returns:
        - The updated instance of AboutUs model.

        """
        
        super().update(instance, validated_data)
        if 'image_file' in validated_data:
            # Get media type from upload license file
            content_type = str(validated_data['image_file'].content_type).split("/")
            if content_type[0] not in ["video", "image"]:
                media_type = 'document'
            else:
                media_type = content_type[0]
            # save media file into media table and get instance of saved data.
            media_instance = Media(title=validated_data['image_file'].name,
                                   file_path=validated_data['image_file'], media_type=media_type)
            media_instance.save()
            # save media instance into license id file into employer profile table.
            instance.image = media_instance
            instance.save()
        return instance


class FaqCategorySerializers(serializers.ModelSerializer):
    """
    Serializer class for the `FaqCategory` model.

    The `FaqCategorySerializers` class extends `serializers.ModelSerializer` and is used to create instances of the
    `FaqCategory` model. It defines the fields that should be included in the serialized representation of the model,
    including 'id', 'title'.
    """

    class Meta:
        model = FaqCategory
        fields = ['id', 'title', 'role']
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
        if FaqCategory.objects.filter(title__iexact=title, is_removed=False).exists():
            raise serializers.ValidationError({'title': title + ' already exist.'})
        return data

    def update(self, instance, validated_data):
        faq_category_instance = super().update(instance, validated_data)
        instance.slug = slugify(faq_category_instance.title)
        instance.save()
        return instance


class FAQSerializers(serializers.ModelSerializer):
    """
    Serializer class for the FAQ model.

    Attributes:
        category (SerializerMethodField): A method field used to serialize the category information.

    Meta:
        model (FAQ): The model associated with the serializer.
        fields (list): The list of fields to include in the serialized representation.
        read_only_fields (list): The list of fields that should be read-only.

    Methods:
        get_category(obj): Custom method to serialize the category information.

    """
    
    category = serializers.SerializerMethodField()
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'category', 'role', 'status']
        read_only_fields = ['id'] 
        
    def get_category(self, obj):
        """
        Retrieve and serialize the category information.

        Args:
            obj: The FAQ object being serialized.

        Returns:
            dict or None: A dictionary containing the category information (id and title),
            or None if no category is associated with the FAQ.

        """
        
        context = {}
        if obj.category:
            context['id'] = obj.category.id
            context['title'] = obj.category.title
            return context
        return None
 

class CreateFAQSerializers(serializers.ModelSerializer):
    """
    Serializer for creating or updating a Frequently Asked Question (FAQ).

    Attributes:
        Meta:
            model (FAQ): The model associated with the serializer.
            fields (list): The fields to include in the serialized data.
            read_only_fields (list): The fields that should be read-only.

    Methods:
        validate(data): Validates the data before creating or updating an FAQ.
        update(instance, validated_data): Updates an existing FAQ instance with the validated data.
    """

    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'category', 'role', 'status']
        read_only_fields = ['id'] 

    def validate(self, data):

        question = data.get("question")
        if FAQ.objects.filter(question__iexact=question, is_removed=False).exists():
            raise serializers.ValidationError({'question': question + ' already exist.'})
        return data

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        return instance


class UploadLogoSerializers(serializers.ModelSerializer):
    """
    Serializes the `Media` model fields for logo data.

    This serializer is used to convert the `Media` model fields into a JSON representation
    for logo data. It specifies the model, `Media`, and the fields to be included
    in the serialized output.

    Attributes:
        model (class): The model class that the serializer is based on.
        fields (list): The list of fields from the `Media` model to be serialized.

    Example:
        serializer = UploadLogoSerializers(data)
        serialized_data = serializer.data

    """
    category_logo = serializers.FileField(
        style={"input_type": "file"},
        write_only=True,
        allow_null=False
    )
    
    class Meta:
        model = CategoryLogo
        fields = ['id', 'category_logo']

    def validate_category_logo(self, category_logo):
        """
        Validates that the uploaded category logo is a valid image file.

        Args:
            - `category_logo (File)`: The category logo file to validate.

        Returns:
            - `File`: The validated category logo file.

        Raises:
            - `ValidationError`: If the category logo file is `blank or invalid`.
        """
        if category_logo in ["", None]:
            raise serializers.ValidationError('Category logo can not be blank.', code='category_logo')
        content_type = str(category_logo.content_type).split("/")
        if content_type[0] == "image":
            return category_logo
        else:
            raise serializers.ValidationError('Invalid category logo.', code='category_logo')

    def save(self):
        category_logo = None
        if 'category_logo' in self.validated_data:
            category_logo = self.validated_data.pop('category_logo')
        category_logo_instance = super().save(status=True)
        if category_logo:
            content_type = str(category_logo.content_type).split("/")
            if content_type[0] not in ["video", "image"]:
                media_type = 'document'
            else:
                media_type = content_type[0]
            # save media file into media table and get instance of saved data.
            media_instance = Media(title=category_logo.name, file_path=category_logo, media_type=media_type)
            media_instance.save()
            # save media instance into license id file into employer profile table.
            category_logo_instance.logo = media_instance
            category_logo_instance.save()
            
            return {"id":category_logo_instance.id, "path":media_instance.file_path.url}
        return None


class LogoSerializers(serializers.ModelSerializer):

    logo = AttachmentSerializer()
    class Meta:
        model = CategoryLogo
        fields = ['id', 'logo']


class GetTestimonialSerializers(serializers.ModelSerializer):
    """
    Serializer for retrieving testimonials.

    This serializer is used to convert Testimonial model instances into JSON-compatible representations.
    It includes a nested image field, serialized using the AttachmentSerializer.

    Attributes:
        - image: An instance of the AttachmentSerializer used to serialize the image field.
    
    Meta:
        - model: The model class to be serialized (Testimonial).
        - fields: The fields to include in the serialized output (id, title, client_name, client_company, 
            client_position, description, image).
        - read_only_fields: The fields that are read-only and should not be modified when deserializing input 
            data (id).
    """
    
    image = AttachmentSerializer()
    class Meta:
        model = Testimonial
        fields = ['id', 'title', 'client_name', 'client_company', 'client_position', 'description', 'image']
        read_only_fields = ['id'] 


class TestimonialSerializers(serializers.ModelSerializer):
    """
    Serializes and deserializes Testimonial objects.

    This class defines the serialization and deserialization behavior for Testimonial objects,
    allowing them to be represented as JSON or validated input data. It provides a file field
    for the testimonial image, allowing file upload and processing.

    Attributes:
        testimonial_image (serializers.FileField): A file field for the testimonial image.
            It specifies the input type as a file and allows only non-null values.

    Meta:
        model (Testimonial): The model class to be serialized/deserialized.
        fields (list): The list of fields to be included in the serialization/deserialization.

    Usage:
        serializer = TestimonialSerializers(data=request.data)
        if serializer.is_valid():
            testimonial = serializer.save()
            # Perform further operations with the serialized testimonial object.

    """
    
    testimonial_image = serializers.FileField(
        style={"input_type": "file"},
        write_only=True,
        allow_null=False
    )

    class Meta:
        model = Testimonial
        fields = ['id', 'title', 'client_name', 'client_company', 'client_position', 'description', 'testimonial_image']

    def validate_testimonial_image(self, testimonial_image):
        """
        Validates the testimonial image provided.

        Parameters:
            testimonial_image (File): The testimonial image to validate.

        Raises:
            serializers.ValidationError: If the testimonial image is blank or not an image.

        Returns:
            File: The validated testimonial image.

        """
    
        if not testimonial_image:
            raise serializers.ValidationError('Testimonial image cannot be blank.', code='testimonial_image')
        content_type = testimonial_image.content_type.split("/")
        if content_type[0] != "image":
            raise serializers.ValidationError('Invalid testimonial image.', code='testimonial_image')
        return testimonial_image

    def save(self):
        """
        Save method for TestimonialSerializers.

        This method saves the testimonial instance along with its associated image.
        It retrieves the testimonial image from the validated data, creates a media instance,
        and links it to the testimonial instance.

        Returns:
            self: The updated TestimonialSerializers instance.

        Raises:
            N/A
        """

        testimonial_image = None
        if 'testimonial_image' in self.validated_data:
            testimonial_image = self.validated_data.pop('testimonial_image')
        testimonial_instance = super().save(status=True)
        if testimonial_image:
            content_type = testimonial_image.content_type.split("/")
            media_type = content_type[0] if content_type[0] in ["video", "image"] else 'document'
            media_instance = Media(title=testimonial_image.name, file_path=testimonial_image, media_type=media_type)
            media_instance.save()
            testimonial_instance.image = media_instance
            testimonial_instance.save()
        return self

    def update(self, instance, validated_data):
        """
        Update an existing Testimonial instance with the provided validated data.
        
        Args:
            self: The TestimonialSerializer instance.
            instance: The Testimonial object to update.
            validated_data: A dictionary of validated data containing the fields to update.
            
        Returns:
            The updated Testimonial instance.
            
        Raises:
            N/A
            
        This method updates the fields of the Testimonial instance based on the provided
        validated data. If there is a 'testimonial_image' field in the validated data, it
        is extracted and used to create a Media instance. The media type of the image is 
        determined based on the content type. The Media instance is then associated with
        the Testimonial instance by assigning it to the 'image' field. The 'slug' field of
        the Testimonial instance is updated with a slugified version of the testimonial
        title. Finally, the updated Testimonial instance is saved and returned.
        """
        
        testimonial_image = None
        if 'testimonial_image' in self.validated_data:
            testimonial_image = self.validated_data.pop('testimonial_image')
        testimonial_instance = super().update(instance, validated_data)
        if testimonial_image:
            content_type = testimonial_image.content_type.split("/")
            media_type = content_type[0] if content_type[0] in ["video", "image"] else 'document'
            media_instance = Media(title=testimonial_image.name, file_path=testimonial_image, media_type=media_type)
            media_instance.save()
            instance.image = media_instance
        instance.slug = slugify(testimonial_instance.title)
        instance.save()
        return instance


class NewsletterUserSerializers(serializers.ModelSerializer):
    """
    Serializer class for the Country model.

    This serializer is used to serialize/deserialize Country objects.
    
    Attributes:
        model (django.db.models.Model): The model class associated with the serializer.
        fields (list): The fields to include in the serialized representation.
        read_only_fields (list): The fields that are read-only and should not be modified during deserialization.
    """

    class Meta:
        model = NewsletterUser
        fields = ['id', 'email', 'created']
        read_only_fields = ['id', 'created']    

