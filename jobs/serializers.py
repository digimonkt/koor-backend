from rest_framework import serializers

from jobs.models import (
    JobDetails, JobAttachmentsItem, JobCategory,
    JobsLanguageProficiency, JobFilters,
    JobSubCategory, JobShare
)

from job_seekers.models import (
    AppliedJob, EducationRecord, JobSeekerLanguageProficiency,
    JobSeekerSkill, AppliedJobAttachmentsItem, SavedJob
)

from project_meta.serializers import (
    CitySerializer, CountrySerializer, LanguageSerializer,
    SkillSerializer, HighestEducationSerializer
)

from users.serializers import UserSerializer, ApplicantDetailSerializers


class AppliedJobAttachmentsSerializer(serializers.ModelSerializer):
    """
    Serializer for the AppliedJobAttachmentsItem model.

    This serializer is used to serialize AppliedJobAttachmentsItem objects to a JSON-compatible format, including
    a link to the attachment file if it exists.

    Attributes:
        attachment: A SerializerMethodField that calls the get_attachment method to retrieve the file path
            of the attachment.

    """
    title = serializers.SerializerMethodField()
    path = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = AppliedJobAttachmentsItem
        fields = (
            'id', 'path', 'title', 'type'
        )

    def get_path(self, obj):
        """
        Retrieves the URL of the attachment file for a AppliedJobAttachmentsItem object, if it exists.

        Args:
            obj: The AppliedJobAttachmentsItem object to retrieve the attachment URL for.

        Returns:
            The URL of the attachment file if it exists, otherwise None.

        """
        if obj.attachment:
            return obj.attachment.file_path.url
        return None

    def get_title(self, obj):
        """
        Retrieves the URL of the attachment file for a AppliedJobAttachmentsItem object, if it exists.

        Args:
            obj: The AppliedJobAttachmentsItem object to retrieve the attachment URL for.

        Returns:
            The URL of the attachment file if it exists, otherwise None.

        """
        if obj.attachment:
            return obj.attachment.title
        return None

    def get_type(self, obj):
        """
        Retrieves the URL of the attachment file for a AppliedJobAttachmentsItem object, if it exists.

        Args:
            obj: The AppliedJobAttachmentsItem object to retrieve the attachment URL for.

        Returns:
            The URL of the attachment file if it exists, otherwise None.

        """
        if obj.attachment:
            return obj.attachment.media_type
        return None


class JobsLanguageProficiencySerializer(serializers.ModelSerializer):
    """
    Serializer for the JobsLanguageProficiency model.

    This serializer is used to serialize/deserialize JobsLanguageProficiency objects to/from JSON format. It defines
    the fields that will be included in the serialized data and provides validation for deserialization.

    Attributes:
        Meta: A subclass of the serializer that specifies the model to be serialized and the fields
            to be included in the serialized data.
    """
    language = serializers.SerializerMethodField()

    class Meta:
        model = JobsLanguageProficiency
        fields = (
            'id', 'language', 'written',
            'spoken'
        )

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

        context = {}
        get_data = LanguageSerializer(obj.language)
        if get_data.data:
            context = get_data.data
        return context


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


class JobSubCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the JobSubCategory model.

    This serializer is used to serialize/deserialize JobSubCategory objects to/from JSON format. It defines
    the fields that will be included in the serialized data and provides validation for deserialization.

    Attributes:
        Meta: A subclass of the serializer that specifies the model to be serialized and the fields
            to be included in the serialized data.
    """
    category = serializers.SerializerMethodField()
    class Meta:
        model = JobSubCategory
        fields = (
            'id',
            'title',
            'category'
        )
    
    def get_category(self, obj):
        
        if obj.category:
            return {'id': obj.category.id, 'title': obj.category.title}
        return None



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
    is_applied = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = JobDetails
        fields = [
            'id', 'title', 'description', 'budget_currency', 'budget_amount',
            'budget_pay_period', 'country', 'city', 'is_full_time', 'is_part_time',
            'has_contract', 'duration', 'experience', 'status', 'applicant', 'deadline', 'start_date',
            'created', 'is_applied', 'is_saved', 'user'
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

    def get_is_applied(self, obj):
        is_applied_record = False
        if 'user' in self.context:
            user = self.context['user']
            if user.is_authenticated:
                is_applied_record = AppliedJob.objects.filter(
                    job=obj,
                    user=user
                ).exists()
        return is_applied_record

    def get_is_saved(self, obj):
        is_saved_record = False
        if 'user' in self.context:
            if self.context['user'].is_authenticated:
                is_saved_record = SavedJob.objects.filter(
                    job=obj,
                    user=self.context['user']
                ).exists()
        return is_saved_record

    def get_applicant(self, obj):
        return AppliedJob.objects.filter(job=obj).count()


class GetJobsDetailSerializers(serializers.ModelSerializer):
    """Serializer for the JobDetails model with additional fields.

    This serializer provides additional fields that are not present in the JobDetails model
    but are computed from related models. These fields include the country, city, job category,
    language, skill, user, applicant, and attachments.

    Attributes:
        country: A SerializerMethodField for the country of the job.
        city: A SerializerMethodField for the city of the job.
        job_category: A SerializerMethodField for the job category or categories of the job.
        job_sub_category: A SerializerMethodField for the job sub category or sub categories of the job.
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
    job_sub_category = serializers.SerializerMethodField()
    highest_education = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()
    skill = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    applicant = serializers.SerializerMethodField()
    attachments = serializers.SerializerMethodField()
    is_applied = serializers.SerializerMethodField()
    application = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = JobDetails
        fields = [
            'id', 'title', 'description', 'budget_currency', 'budget_amount', 'budget_pay_period',
            'country', 'city', 'address', 'job_category', 'job_sub_category', 'is_full_time', 'is_part_time', 'has_contract',
            'contact_email', 'cc1', 'cc2', 'contact_whatsapp', 'highest_education', 'language', 'skill',
            'duration', 'experience', 'status', 'applicant', 'deadline', 'start_date', 'created', 'user', 'attachments',
            'is_applied', 'application', 'is_saved'

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
        if obj.country:
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
        if obj.city:
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

        context = {}
        get_data = JobCategorySerializer(obj.job_category, many=True)
        if get_data.data:
            context = get_data.data[0]
        return context

    def get_job_sub_category(self, obj):
        """Get the serialized job sub category data for a JobDetails object.

        This method uses the JobSubCategorySerializer to serialize the job sub categories associated with a JobDetails
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A JobDetails object whose job sub category data will be serialized.

        Returns:
            A dictionary containing the serialized job sub category data, or an empty dictionary if the
            serializer did not return any data.

        """

        context = {}
        get_data = JobSubCategorySerializer(obj.job_sub_category, many=True)
        if get_data.data:
            context = get_data.data[0]
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
        if obj.highest_education:
            get_data = HighestEducationSerializer(obj.highest_education)
            if get_data.data:
                context = get_data.data
        return context

    def get_language(self, obj):
        """Get the serialized language data for a JobDetails object.

        This method uses the JobsLanguageProficiencySerializer to serialize the languages associated with a JobDetails
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A JobDetails object whose language data will be serialized.

        Returns:
            A dictionary containing the serialized language data, or an empty dictionary if the
            serializer did not return any data.

        """

        context = []
        data = JobsLanguageProficiency.objects.filter(job=obj)
        get_data = JobsLanguageProficiencySerializer(data, many=True)
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
        if obj.skill:
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
        if obj.user:
            get_data = UserSerializer(obj.user)
            if get_data.data:
                context = get_data.data
        return context

    def get_applicant(self, obj):
        return AppliedJob.objects.filter(job=obj).count()

    def get_is_applied(self, obj):
        is_applied_record = False
        if 'user' in self.context:
            user = self.context['user']
            is_applied_record = AppliedJob.objects.filter(
                job=obj,
                user=user
            ).exists()
        return is_applied_record
    
    def get_application(self, obj):
        application_context = dict()
        if 'user' in self.context:
            user = self.context['user']
            if AppliedJob.objects.filter(job=obj, user=user).exists():
                application = AppliedJob.objects.get(job=obj, user=user)
                application_context['id'] = application.id
                application_context['created'] = application.created
        return application_context

    def get_is_saved(self, obj):
        is_saved_record = False
        if 'user' in self.context:
            user = self.context['user']
            is_saved_record = SavedJob.objects.filter(
                job=obj,
                user=user
            ).exists()
        return is_saved_record

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


class AppliedJobSerializers(serializers.ModelSerializer):
    """
    A serializer class for serializing `AppliedJob` instances with additional information about the job seeker's
    education, language proficiency, and skills.

    This serializer includes the following fields:
        - `id`: the ID of the AppliedJob instance.
        - `shortlisted_at`: the datetime when the job seeker was shortlisted for the job.
        - `rejected_at`: the datetime when the job seeker was rejected for the job.
        - `created`: the datetime when the AppliedJob instance was created.
        - `short_letter`: the cover letter submitted by the job seeker.
        - `user`: a nested serialization of the job seeker's user profile, including
                the user's ID, email, first name, last name, and profile picture.
        - `education`: a boolean value indicating whether the job seeker has an
                     education record matching the required education level of the job.
        - `language`: a boolean value indicating whether the job seeker has language
                    proficiency in any of the required languages for the job.
        - `skill`: a boolean value indicating whether the job seeker has any of the
                 required skills for the job.

    The `get_user`, `get_education`, `get_language`, and `get_skill` methods are used
    to customize the serialization of the `user`, `education`, `language`, and `skill` fields,
    respectively.

    """
    user = serializers.SerializerMethodField()
    education = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()
    skill = serializers.SerializerMethodField()
    job = serializers.SerializerMethodField()

    class Meta:
        model = AppliedJob
        fields = [
            'id', 'shortlisted_at', 'rejected_at', 'interview_at', 'created', 
            'short_letter', 'user', 'education', 'language', 'skill', 'job'
        ]

    def get_user(self, obj):
        """
        A method for customizing the serialization of the `user` field.

        This method returns a serialized representation of the job seeker's user profile, including the user's ID,
        email, first name, last name, and profile picture.

        Args:
            - `obj`: the AppliedJob instance being serialized.

        Returns:
            - A dictionary containing the serialized user profile information.

        """
        context = {}
        get_data = UserSerializer(obj.user)
        if get_data.data:
            context = get_data.data
        return context

    def get_education(self, obj):
        """
        A method for customizing the serialization of the `education` field.

        This method returns a boolean value indicating whether the job seeker has an education record matching the
        required education level of the job.

        Args:
            - `obj`: the AppliedJob instance being serialized.

        Returns:
            - A boolean value indicating whether the job seeker has the required education level.

        """
        education_record = EducationRecord.objects.filter(
            user=obj.user,
            education_level=obj.job.highest_education
        ).exists()
        return education_record

    def get_language(self, obj):
        """
        A method for customizing the serialization of the `language` field.

        This method returns a boolean value indicating whether the job seeker has language proficiency in any of the
        required languages for the job.

        Args:
            - `obj`: the AppliedJob instance being serialized.

        Returns:
            - A boolean value indicating whether the job seeker has language proficiency in any of the required
            languages for the job.

        """
        language_list = []
        data = JobsLanguageProficiency.objects.filter(job=obj.job)
        for get_data in data:
            language_list.append(get_data.language)
        language_record = JobSeekerLanguageProficiency.objects.filter(
            user=obj.user,
            language__in=language_list
        ).exists()
        return language_record

    def get_skill(self, obj):
        """
        A method for customizing the serialization of the `skill` field.

        This method returns a boolean value indicating whether the job seeker has skill proficiency in any of the
        required skills for the job.

        Args:
            - `obj`: the AppliedJob instance being serialized.

        Returns:
            - A boolean value indicating whether the job seeker has skill proficiency in any of the required
            skills for the job.

        """
        skill_record = JobSeekerSkill.objects.filter(
            user=obj.user,
            skill__in=obj.job.skill.all()
        ).exists()
        return skill_record

    def get_job(self, obj):
        """
        A method for customizing the serialization of the `skill` field.

        This method returns a boolean value indicating whether the job seeker has skill proficiency in any of the
        required skills for the job.

        Args:
            - `obj`: the AppliedJob instance being serialized.

        Returns:
            - A boolean value indicating whether the job seeker has skill proficiency in any of the required
            skills for the job.

        """
        return {"id": obj.job.id, "title": obj.job.title}


class GetAppliedJobsSerializers(serializers.ModelSerializer):
    """
    A serializer class for the AppliedJob model that returns details of applied jobs.

    This serializer includes the following fields:
        - id (int): The ID of the applied job.
        - shortlisted_at (datetime): The date and time when the job was shortlisted.
        - rejected_at (datetime): The date and time when the job was rejected.
        - short_letter (str): The short letter submitted with the job application.
        - attachments (list): A list of URLs for any attachments submitted with the job application.
        - job (dict): A dictionary containing details of the job posting.

    The 'job' field is a serialized representation of the related JobDetails object, and is populated
    using the `get_job` method of the GetAppliedJobsSerializers class.
    """

    user = serializers.SerializerMethodField()
    job = serializers.SerializerMethodField()
    attachments = serializers.SerializerMethodField()

    class Meta:
        model = AppliedJob
        fields = ['id', 'shortlisted_at', 'rejected_at', 'short_letter', 'created', 'attachments', 'job', 'user']

    def get_attachments(self, obj):
        """Get the serialized attachment data for a AppliedJob object.

        This method uses the JobAttachmentsItem model to retrieve the attachments associated with a AppliedJob
        object. It then uses the AppliedJobAttachmentsSerializer to serialize the attachment data. If the serializer
        returns data, the first attachment in the list is extracted and added to a list, which is then returned.

        Args:
            obj: A AppliedJob object whose attachment data will be serialized.

        Returns:
            A list containing the first serialized attachment data, or an empty list if the serializer did
            not return any data.

        """

        context = []
        attachments_data = AppliedJobAttachmentsItem.objects.filter(applied_job=obj)
        get_data = AppliedJobAttachmentsSerializer(attachments_data, many=True)
        if get_data.data:
            context = get_data.data
        return context

    def get_job(self, obj):
        """
        Returns a dictionary with details of a job posting.

        Args:
            obj: An object representing a job application.

        Returns:
            A dictionary containing details of the job posting, such as the job title, company name,
            job location, etc.

        If the job posting does not exist, an empty dictionary will be returned.
        """
        return {"id": obj.job.id, "title": obj.job.title}

    def get_user(self, obj):
        context = {}
        get_data = ApplicantDetailSerializers(obj.user)
        if get_data.data:
            context = get_data.data
        return context


class JobFiltersSerializers(serializers.ModelSerializer):
    """
    JobFiltersSerializers is a class-based serializer that inherits from the ModelSerializer class of the Django REST
    Framework.
    It defines a Meta class that specifies the JobFilters model and the fields to be included in the serialization.

    Attributes:
        - `model (class)`: The Django model class that this serializer is based on.
        - `fields (list)`: A list of fields to be included in the serialized output.
        
    Usage:
        - This serializer can be used to serialize JobFilters objects and convert them to JSON format for use in HTTP
        requests and responses.
    """

    class Meta:
        model = JobFilters
        fields = [
            'id', 'title', 'country', 'city', 'job_category', 'job_sub_category',
            'is_full_time', 'is_part_time', 'has_contract', 'is_notification',
            'salary_min', 'salary_max', 'duration'
        ]

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        return instance


class GetJobFiltersSerializers(serializers.ModelSerializer):
    """
    `GetJobFiltersSerializers` is a class-based serializer that inherits from the `ModelSerializer` class of the
    Django REST Framework.
    It defines a Meta class that specifies the JobFilters model and the fields to be included in the serialization,
    as well as additional SerializerMethodFields.

    Attributes:
        - `model (class)`: The Django model class that this serializer is based on.
        - `fields (list)`: A list of fields to be included in the serialized output, including additional fields
            generated by `SerializerMethodFields`.

    Usage:
        - This serializer can be used to serialize JobFilters objects and convert them to JSON format for use in HTTP
            responses.
        - In addition to the standard fields specified in the Meta class, this serializer also includes
            `SerializerMethodFields` for 'country', 'city', and 'job_category' 'job_sub_category'.
        - These fields are generated by calling the corresponding methods on the serializer instance and returning
            their values.
        - The resulting serialized output will include the standard fields as well as the additional fields generated
            by the SerializerMethodFields.
    """

    country = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    job_category = serializers.SerializerMethodField()
    job_sub_category = serializers.SerializerMethodField()

    class Meta:
        model = JobFilters
        fields = [
            'id', 'title', 'country', 'city', 'job_category', 'job_sub_category',
            'is_full_time', 'is_part_time', 'has_contract', 'is_notification',
            'duration'
        ]

    def get_country(self, obj):
        """Get the serialized country data for a JobFilters object.

        This method uses the CountrySerializer to serialize the country associated with a JobFilters
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A JobFilters object whose country data will be serialized.

        Returns:
            A dictionary containing the serialized country data, or an empty dictionary if the
            serializer did not return any data.

        """
        context = {}
        if obj.country:
            get_data = CountrySerializer(obj.country)
            if get_data.data:
                context = get_data.data
        return context

    def get_city(self, obj):
        """Get the serialized city data for a JobFilters object.

        This method uses the CitySerializer to serialize the city associated with a JobFilters
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A JobFilters object whose city data will be serialized.

        Returns:
            A dictionary containing the serialized city data, or an empty dictionary if the
            serializer did not return any data.

        """

        context = {}
        if obj.city:
            get_data = CitySerializer(obj.city)
            if get_data.data:
                context = get_data.data
        return context

    def get_job_category(self, obj):
        """Get the serialized job category data for a JobFilters object.

        This method uses the JobCategorySerializer to serialize the job categories associated with a JobFilters
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A JobFilters object whose job category data will be serialized.

        Returns:
            A dictionary containing the serialized job category data, or an empty dictionary if the
            serializer did not return any data.

        """

        context = []
        get_data = JobCategorySerializer(obj.job_category, many=True)
        if get_data.data:
            context = get_data.data
        return context

    def get_job_sub_category(self, obj):
        """Get the serialized job sub category data for a JobFilters object.

        This method uses the JobSubCategorySerializer to serialize the job sub categories associated with a JobFilters
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A JobFilters object whose job sub category data will be serialized.

        Returns:
            A dictionary containing the serialized job sub category data, or an empty dictionary if the
            serializer did not return any data.

        """

        context = []
        get_data = JobSubCategorySerializer(obj.job_sub_category, many=True)
        if get_data.data:
            context = get_data.data
        return context


class ShareCountSerializers(serializers.ModelSerializer):

    total = serializers.SerializerMethodField()

    class Meta:
        model = JobShare
        fields = [
            'whatsapp', 'telegram', 'facebook', 'linked_in',
            'mail', 'direct_link', 'total'
        ]

    def get_total(self, obj):
        return obj.whatsapp + obj.telegram + obj.facebook + obj.linked_in + obj.mail + obj.direct_link
