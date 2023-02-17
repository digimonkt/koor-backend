from rest_framework import serializers

from jobs.models import JobDetails, JobAttachmentsItem, JobCategory
from project_meta.serializers import (
    CitySerializer, CountrySerializer, LanguageSerializer,
    SkillSerializer, HighestEducationSerializer
)
from users.serializers import UserSerializer


class JobCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the JobCategory model.

    This serializer is used to serialize/deserialize JobCategory objects to/from JSON format. It defines
    the fields that will be included in the serialized data and provides validation for deserialization.

    Attributes:
        Meta: A subclass of the serializer that specifies the model to be serialized and the fields
            to be included in the serialized data.
    """

    class Meta:
        model = JobCategory
        fields = (
            'id',
            'title',
        )


class AttachmentsSerializer(serializers.ModelSerializer):
    """
    Serializer for the JobAttachmentsItem model.

    This serializer is used to serialize JobAttachmentsItem objects to a JSON-compatible format, including
    a link to the attachment file if it exists.

    Attributes:
        attachment: A SerializerMethodField that calls the get_attachment method to retrieve the file path
            of the attachment.

    """
    title = serializers.SerializerMethodField()
    path = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = JobAttachmentsItem
        fields = (
            'id', 'path', 'title', 'type'
        )

    def get_path(self, obj):
        """
        Retrieves the URL of the attachment file for a JobAttachmentsItem object, if it exists.

        Args:
            obj: The JobAttachmentsItem object to retrieve the attachment URL for.

        Returns:
            The URL of the attachment file if it exists, otherwise None.

        """
        if obj.attachment:
            return obj.attachment.file_path.url
        return None
    
    def get_title(self, obj):
        """
        Retrieves the URL of the attachment file for a JobAttachmentsItem object, if it exists.

        Args:
            obj: The JobAttachmentsItem object to retrieve the attachment URL for.

        Returns:
            The URL of the attachment file if it exists, otherwise None.

        """
        if obj.attachment:
            return obj.attachment.title
        return None
    
    def get_type(self, obj):
        """
        Retrieves the URL of the attachment file for a JobAttachmentsItem object, if it exists.

        Args:
            obj: The JobAttachmentsItem object to retrieve the attachment URL for.

        Returns:
            The URL of the attachment file if it exists, otherwise None.

        """
        if obj.attachment:
            return obj.attachment.media_type
        return None


class GetJobsSerializers(serializers.ModelSerializer):
    """
    Serializer for the JobDetails model.

    This serializer is used to serialize JobDetails objects to a JSON-compatible format, including
    related objects such as the country, city, user, and applicant. The `get_country`, `get_city`,
    and `get_user` methods use related serializers to retrieve the related data and add it to the
    serialized output.

    Attributes:
        country: A SerializerMethodField that calls the `get_country` method to retrieve the country data.
        city: A SerializerMethodField that calls the `get_city` method to retrieve the city data.
        user: A SerializerMethodField that calls the `get_user` method to retrieve the user data.
        applicant: A SerializerMethodField that returns a default value of 0.

    """
    country = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    applicant = serializers.SerializerMethodField()

    class Meta:
        model = JobDetails
        fields = [
            'id', 'title', 'description', 'budget_currency', 'budget_amount',
            'budget_pay_period', 'country', 'city', 'is_full_time', 'is_part_time',
            'has_contract', 'working_days', 'status', 'applicant', 'deadline', 'created', 'user'
        ]

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
        """
        Retrieves the serialized data for the user related to a JobDetails object.

        Args:
            obj: The JobDetails object to retrieve the user data for.

        Returns:
            A dictionary containing the serialized user data.

        """

        context = {}
        get_data = UserSerializer(obj.user)
        if get_data.data:
            context = get_data.data
        return context

    def get_applicant(self, obj):
        return 0


class GetJobsDetailSerializers(serializers.ModelSerializer):
    """Serializer for the JobDetails model with additional fields.

    This serializer provides additional fields that are not present in the JobDetails model
    but are computed from related models. These fields include the country, city, job category,
    language, skill, user, applicant, and attachments.

    Attributes:
        country: A SerializerMethodField for the country of the job.
        city: A SerializerMethodField for the city of the job.
        job_category: A SerializerMethodField for the job category or categories of the job.
        language: A SerializerMethodField for the language or languages required for the job.
        skill: A SerializerMethodField for the skill or skills required for the job.
        user: A SerializerMethodField for the user who posted the job.
        applicant: A SerializerMethodField that always returns 0, as there is no applicant data
            included in this serializer.
        attachments: A SerializerMethodField for the attachments associated with the job.

    """

    country = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    job_category = serializers.SerializerMethodField()
    highest_education = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()
    skill = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    applicant = serializers.SerializerMethodField()
    attachments = serializers.SerializerMethodField()

    class Meta:
        model = JobDetails
        fields = [
            'id', 'title', 'description', 'budget_currency', 'budget_amount', 'budget_pay_period',
            'country', 'city', 'address', 'job_category', 'is_full_time', 'is_part_time', 'has_contract',
            'contact_email', 'contact_phone', 'contact_whatsapp', 'highest_education', 'language', 'skill',
            'working_days', 'status', 'applicant', 'deadline', 'created', 'user', 'attachments'

        ]

    def get_country(self, obj):
        """Get the serialized country data for a JobDetails object.

        This method uses the CountrySerializer to serialize the country associated with a JobDetails
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A JobDetails object whose country data will be serialized.

        Returns:
            A dictionary containing the serialized country data, or an empty dictionary if the
            serializer did not return any data.

        """
        context = {}
        get_data = CountrySerializer(obj.country)
        if get_data.data:
            context = get_data.data
        return context

    def get_city(self, obj):
        """Get the serialized city data for a JobDetails object.

        This method uses the CitySerializer to serialize the city associated with a JobDetails
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A JobDetails object whose city data will be serialized.

        Returns:
            A dictionary containing the serialized city data, or an empty dictionary if the
            serializer did not return any data.

        """

        context = {}
        get_data = CitySerializer(obj.city)
        if get_data.data:
            context = get_data.data
        return context

    def get_job_category(self, obj):
        """Get the serialized job category data for a JobDetails object.

        This method uses the JobCategorySerializer to serialize the job categories associated with a JobDetails
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A JobDetails object whose job category data will be serialized.

        Returns:
            A dictionary containing the serialized job category data, or an empty dictionary if the
            serializer did not return any data.

        """

        context = []
        get_data = JobCategorySerializer(obj.job_category, many=True)
        if get_data.data:
            context = get_data.data
        return context
    
    def get_highest_education(self, obj):
        """Get the serialized highest education data for a JobDetails object.

        This method uses the HighestEducationSerializer to serialize the highest educations associated with a JobDetails
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A JobDetails object whose highest education data will be serialized.

        Returns:
            A dictionary containing the serialized highest education data, or an empty dictionary if the
            serializer did not return any data.

        """

        context = {}
        get_data = HighestEducationSerializer(obj.highest_education)
        if get_data.data:
            context = get_data.data
        return context

    def get_language(self, obj):
        """Get the serialized language data for a JobDetails object.

        This method uses the LanguageSerializer to serialize the languages associated with a JobDetails
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A JobDetails object whose language data will be serialized.

        Returns:
            A dictionary containing the serialized language data, or an empty dictionary if the
            serializer did not return any data.

        """

        context = []
        get_data = LanguageSerializer(obj.language, many=True)
        if get_data.data:
            context = get_data.data
        return context

    def get_skill(self, obj):
        """Get the serialized skill data for a JobDetails object.

        This method uses the SkillSerializer to serialize the skills associated with a JobDetails
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A JobDetails object whose skill data will be serialized.

        Returns:
            A dictionary containing the serialized skill data, or an empty dictionary if the
            serializer did not return any data.

        """

        context = []
        get_data = SkillSerializer(obj.skill, many=True)
        if get_data.data:
            context = get_data.data
        return context

        # return obj.city.title

    def get_user(self, obj):
        """Get the serialized user data for a JobDetails object.

        This method uses the UserSerializer to serialize the users associated with a JobDetails
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A JobDetails object whose user data will be serialized.

        Returns:
            A dictionary containing the serialized user data, or an empty dictionary if the
            serializer did not return any data.

        """

        context = {}
        get_data = UserSerializer(obj.user)
        if get_data.data:
            context = get_data.data
        return context

    def get_applicant(self, obj):
        return 0

    def get_attachments(self, obj):
        """Get the serialized attachment data for a JobDetails object.

        This method uses the JobAttachmentsItem model to retrieve the attachments associated with a JobDetails
        object. It then uses the AttachmentsSerializer to serialize the attachment data. If the serializer
        returns data, the first attachment in the list is extracted and added to a list, which is then returned.

        Args:
            obj: A JobDetails object whose attachment data will be serialized.

        Returns:
            A list containing the first serialized attachment data, or an empty list if the serializer did
            not return any data.

        """

        context = []
        attachments_data = JobAttachmentsItem.objects.filter(job=obj)
        get_data = AttachmentsSerializer(attachments_data, many=True)
        if get_data.data:
            context = get_data.data
        return context
