from rest_framework import serializers

from core.emails import get_email_object
from koor.config.common import Common

from jobs.models import JobDetails, JobSubCategory, JobCategory
from project_meta.models import (
    Media, Language

)
from user_profile.models import JobSeekerProfile

from users.serializers import ApplicantDetailSerializers

from jobs.serializers import GetJobsDetailSerializers, GetJobsSerializers, AppliedJobAttachmentsSerializer

from notification.models import Notification

from .models import (
    EducationRecord, JobSeekerLanguageProficiency, EmploymentRecord,
    JobSeekerSkill, AppliedJob, AppliedJobAttachmentsItem,
    SavedJob, JobPreferences, Categories, CoverLetter
)


class UpdateResumeDataSerializers(serializers.ModelSerializer):
    reference = serializers.ListField(
        style={"input_type": "text"},
        write_only=True,
        allow_null=False
    )

    class Meta:
        model = JobSeekerProfile
        fields = ['profile_title', 'short_summary', 'home_address',
                  'personal_website',
                  'reference'
                  ]

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        reference = validated_data.get("reference")
        print(reference)
        if reference:
            for get_reference in reference:
                Reference.objects.create(
                    user=instance.user, 
                    email=get_reference['email'], 
                    mobile_number=get_reference['mobile_number'], 
                    country_code=get_reference['country_code'], 
                    name=get_reference['name']
                )
                
        return instance


class CoverLetterSerializers(serializers.ModelSerializer):
    
    profile_title = serializers.CharField(
        style={"input_type": "text"},
        write_only=True,
        allow_blank=False
    )
    signature_file = serializers.FileField(
        style={"input_type": "file"},
        write_only=True,
        allow_null=False
    )

    class Meta:
        model = CoverLetter
        fields = ['signature_file', 'profile_title', 'name_or_address',
                  'cover_letter'
                  ]
    
    def validate_signature_file(self, signature_file):

        if signature_file in ["", None]:
            raise serializers.ValidationError('Signature can not be blank.', code='signature_file')
        content_type = str(signature_file.content_type).split("/")
        if content_type[0] == "image":
            return signature_file
        else:
            raise serializers.ValidationError('Invalid signature.', code='signature_file')

    def save(self, user, job_instance):
        instance = super().save(user=user, job=job_instance)
        if 'profile_title' in validated_data:
            JobSeekerProfile.objects.filter(user=user).update(profile_title=validated_data['profile_title'])
        if 'signature_file' in validated_data:
            # Get media type from upload license file
            content_type = str(validated_data['signature_file'].content_type).split("/")
            if content_type[0] not in ["video", "image"]:
                media_type = 'document'
            else:
                media_type = content_type[0]
            # save media file into media table and get instance of saved data.
            media_instance = Media(title=validated_data['signature_file'].name,
                                   file_path=validated_data['signature_file'], media_type=media_type)
            media_instance.save()
            # save media instance into license id file into employer profile table.
            instance.image = media_instance
            instance.save()
        return self



class UpdateAboutSerializers(serializers.ModelSerializer):
    """
    A serializer for updating JobSeekerProfile instances, including the name of the associated User.

    Attributes:
        full_name: A CharField for the full name of the JobSeekerProfile, used to update the associated User's name.

    Meta:
        model: The JobSeekerProfile model to be serialized.
        fields: The fields of the JobSeekerProfile to be included in the serializer.

    Methods:
        update: Update the JobSeekerProfile instance with the provided validated data, and update the associated User's name if the full_name field is included.

    Returns:
        The updated JobSeekerProfile instance.
    """

    full_name = serializers.CharField(
        style={"input_type": "text"},
        write_only=True,
        allow_blank=False
    )
    # email = serializers.CharField(
    #     style={"input_type": "text"},
    #     write_only=True,
    #     allow_blank=False
    # )
    mobile_number = serializers.CharField(
        style={"input_type": "text"},
        write_only=True,
        allow_blank=False
    )
    country_code = serializers.CharField(
        style={"input_type": "text"},
        write_only=True,
        allow_blank=False
    )

    class Meta:
        model = JobSeekerProfile
        fields = ['gender', 'dob', 'employment_status', 'description',
                  'market_information_notification', 'job_notification',
                  'full_name', 'mobile_number', 'country_code',
                  'highest_education', 'country', 'city', 'experience',
                  'profile_title'
                  ]

    def validate_mobile_number(self, mobile_number):
        if mobile_number != '':
            if mobile_number.isdigit():
                return mobile_number
            else:
                raise serializers.ValidationError('mobile_number must contain only numbers', code='mobile_number')
        else:
            raise serializers.ValidationError('mobile_number can not be blank', code='mobile_number')

    # def validate_email(self, email):
    #     if email != '':
    #         return email
    #     else:
    #         raise serializers.ValidationError('email can not be blank', code='email')

    def validate(self, data):
        country_code = data.get("country_code")
        mobile_number = data.get("mobile_number")
        if mobile_number and country_code in ["", None]:
            raise serializers.ValidationError({'country_code': 'country code can not be blank'})
        return data

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        if 'full_name' in validated_data:
            instance.user.name = validated_data['full_name']
            instance.user.save()
        # if 'email' in validated_data:
        #     instance.user.email = validated_data['email']
        #     instance.user.save()
        if 'mobile_number' in validated_data:
            instance.user.mobile_number = validated_data['mobile_number']
            instance.user.country_code = validated_data['country_code']
            instance.user.save()
        return instance


class EducationSerializers(serializers.ModelSerializer):
    """ 
    A serializer class for the `EducationRecord` model to convert model instances into JSON serializable data and vice
    versa.

    Attributes: 
        - `Meta (inner class)`: Specifies the metadata for the serializer, including the model to use, and the fields
                                to include in the serialized data.

        - `model (EducationRecord)`: The model class that the serializer should use.

        - `fields (list)`: The list of fields to include in the serialized data. 

    Returns: 
        Serialized data of the EducationRecord model instance in `JSON format`. 
    """

    class Meta:
        model = EducationRecord
        fields = ['id', 'title', 'start_date', 'end_date', 'institute', 'education_level']

    def update(self, instance, validated_data):
        """
        Update the given instance with the validated data and return it.

        Parameters:
            instance : object
                The instance to be updated.
            validated_data : dict
                The validated data to be used to update the instance.

        Returns:
            object
                The updated instance.

        Note:
            This method overrides the update() method of the superclass.
        """

        super().update(instance, validated_data)
        return instance


class JobSeekerLanguageProficiencySerializers(serializers.ModelSerializer):
    """ 
    A serializer class for the `Language` model to convert model instances into JSON serializable data and vice
    versa.

    Attributes: 
        - `Meta (inner class)`: Specifies the metadata for the serializer, including the model to use, and the fields
                                to include in the serialized data.

        - `model (Language)`: The model class that the serializer should use.

        - `fields (list)`: The list of fields to include in the serialized data. 

    Returns: 
        Serialized data of the Language model instance in `JSON format`. 
    """

    class Meta:
        model = JobSeekerLanguageProficiency
        fields = ['id', 'language', 'written', 'spoken']

    def validate_language(self, language):
        if language not in [None, ""]:
            try:
                if Language.objects.get(title=language):
                    return language
            except Language.DoesNotExist:
                raise serializers.ValidationError('Language does not exist.', code='language')
        else:
            raise serializers.ValidationError('Language can not be blank.', code='language')

    def update(self, instance, validated_data):
        """
        Update the given instance with the validated data and return it.

        Parameters:
            instance : object
                The instance to be updated.
            validated_data : dict
                The validated data to be used to update the instance.

        Returns:
            object
                The updated instance.

        Note:
            This method overrides the update() method of the superclass.
        """

        super().update(instance, validated_data)
        return instance


class EmploymentRecordSerializers(serializers.ModelSerializer):
    """ 
    A serializer class for the `EmploymentRecord` model to convert model instances into JSON serializable data and vice
    versa.

    Attributes: 
        - `Meta (inner class)`: Specifies the metadata for the serializer, including the model to use, and the fields
                                to include in the serialized data.

        - `model (EmploymentRecord)`: The model class that the serializer should use.

        - `fields (list)`: The list of fields to include in the serialized data. 

    Returns: 
        Serialized data of the EmploymentRecord model instance in `JSON format`. 
    """

    class Meta:
        model = EmploymentRecord
        fields = ['id', 'title', 'start_date', 'end_date', 'organization', 'description']

    def update(self, instance, validated_data):
        """
        Update the given instance with the validated data and return it.

        Parameters:
            instance : object
                The instance to be updated.
            validated_data : dict
                The validated data to be used to update the instance.

        Returns:
            object
                The updated instance.

        Note:
            This method overrides the update() method of the superclass.
        """

        super().update(instance, validated_data)
        return instance


class JobSeekerSkillSerializers(serializers.ModelSerializer):
    """
    The JobSeekerSkillSerializers class is a Django REST Framework serializer that handles the serialization and
    validation of JobSeekerSkill objects.

    It includes two ListField attributes, skill_add and skill_remove, which are used for adding and removing skills
    from a JobSeekerSkill object.

    The validate() method is used to validate the input data and perform any necessary database operations. If a skill
    is marked for removal, the method deletes the JobSeekerSkill object with the matching skill. The method returns the
    list of skills to be added.

    Attributes:
        - skill_add: a ListField attribute used for adding new skills to a JobSeekerSkill object
        - skill_remove: a ListField attribute used for removing existing skills from a JobSeekerSkill object

    Methods:
        - validate(data): validates input data and performs any necessary database operations

    Usage:
        The JobSeekerSkillSerializers can be used to serialize and validate JobSeekerSkill objects for use in Django
        REST Framework APIs.
    """
    skill_add = serializers.ListField(
        style={"input_type": "text"},
        write_only=True,
        allow_null=False
    )
    skill_remove = serializers.ListField(
        style={"input_type": "text"},
        write_only=True,
        allow_null=False
    )

    class Meta:
        model = JobSeekerSkill
        fields = ['id', 'skill_remove', 'skill_add']

    def validate(self, data):
        skill_add = data.get("skill_add")
        skill_remove = data.get("skill_remove")
        if skill_remove:
            for remove in skill_remove:
                JobSeekerSkill.objects.filter(id=remove).delete()
        return skill_add


class AppliedJobSerializers(serializers.ModelSerializer):
    """Serializer class for serializing and deserializing AppliedJob instances.

    This serializer class defines a ListField for attachments which allows files to be uploaded via a file input field.
    The attachments field is write-only and not required, but must not be null if present.

    Attributes:
        attachments (ListField): A ListField instance with style "input_type": "file", write_only=True,
            allow_null=False, and required=False.
        Meta (Meta): A nested class that defines metadata options for the serializer, including the model class and the
            fields to include in the serialized representation.

    Usage:
        To serialize an AppliedJob instance, create an instance of this serializer and pass the instance to the data
        parameter.
    """

    attachments = serializers.ListField(
        style={"input_type": "file"},
        write_only=True,
        allow_null=False,
        required=False
    )

    class Meta:
        model = AppliedJob
        fields = ['id', 'attachments', 'short_letter']

    def save(self, user, job_instance):
        """Saves a new instance of the AppliedJob model with the given user and job instance, and saves any attachments
        to the job application.

        Args:
            user (User): The user instance to associate with the job application.
            job_instance (Job): The job instance to associate with the job application.

        Returns:
            This instance of the AppliedJobSerializers.

        Behavior:
            This method saves a new instance of the AppliedJob model with the given user and job instance. If there are
            any attachments included in the validated data, each attachment is saved as a media instance and associated
            with the job application by creating an AppliedJobAttachmentsItem instance.

            The method returns the current instance of the serializer.

        Raises:
            Any exceptions raised during the save process.

        Usage:
            To create a new AppliedJob instance and save attachments, call this method on an instance of
            AppliedJobSerializers.

        """

        attachments = None
        if 'attachments' in self.validated_data:
            attachments = self.validated_data.pop('attachments')
        applied_job_instance = super().save(user=user, job=job_instance)
        if job_instance.user:
            if job_instance.user.get_notification:
                Notification.objects.create(
                    user=job_instance.user, application=applied_job_instance,
                    notification_type='applied', created_by=user, job=job_instance
                )
                user_email = []
                if job_instance.user.email:
                    user_email.append(job_instance.user.email)
                if job_instance.contact_email:
                    user_email.append(job_instance.contact_email)
                if job_instance.cc1:
                    user_email.append(job_instance.cc1)
                if job_instance.cc2:
                    user_email.append(job_instance.cc2)
                if user_email:
                    email_context = dict()
                    if job_instance.user.name:
                        user_name = job_instance.user.name
                    elif job_instance.company:
                        user_name = job_instance.company
                    else:
                        user_name = user_email[0]
                    email_context["yourname"] = user_name
                    email_context["username"] = user
                    email_context["resume_link"] = Common.BASE_URL  + "/api/v1/users/job-seeker/resume/user-id?user-id=" + str(user.id)
                    email_context["notification_type"] = "applied job"
                    email_context["job_instance"] = job_instance
                    get_email_object(
                        subject=f'Notification for applied job',
                        email_template_name='email-templates/mail-for-apply-job.html',
                        context=email_context,
                        to_email=user_email
                    )
        else:
            user_email = []
            if job_instance.user:
                if job_instance.user.email:
                    user_email.append(job_instance.user.email)
            if job_instance.contact_email:
                user_email.append(job_instance.contact_email)
            if job_instance.cc1:
                user_email.append(job_instance.cc1)
            if job_instance.cc2:
                user_email.append(job_instance.cc2)
            if user_email:
                email_context = dict()
                if job_instance.user:
                    if job_instance.user.name:
                        user_name = job_instance.user.name
                    else:
                        user_name = user_email[0]
                elif job_instance.company:
                    user_name = job_instance.company
                else:
                    user_name = user_email[0]
                email_context["yourname"] = user_name
                email_context["username"] = user
                email_context["resume_link"] = Common.BASE_URL  + "/api/v1/users/job-seeker/resume/user-id?user-id=" + str(user.id)
                email_context["notification_type"] = "applied job"
                email_context["job_instance"] = job_instance
                get_email_object(
                    subject=f'Notification for applied job',
                    email_template_name='email-templates/mail-for-apply-job.html',
                    context=email_context,
                    to_email=user_email
                )
        if attachments:
            for attachment in attachments:
                content_type = str(attachment.content_type).split("/")
                if content_type[0] not in ["video", "image"]:
                    media_type = 'document'
                else:
                    media_type = content_type[0]
                # save media file into media table and get instance of saved data.
                media_instance = Media(title=attachment.name, file_path=attachment, media_type=media_type)
                media_instance.save()
                # save media instance into license id file into employer profile table.
                attachments_instance = AppliedJobAttachmentsItem.objects.create(applied_job=applied_job_instance,
                                                                                attachment=media_instance)
                attachments_instance.save()
        return self


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

    job = serializers.SerializerMethodField()
    attachments = serializers.SerializerMethodField()

    class Meta:
        model = AppliedJob
        fields = ['id', 'shortlisted_at', 'rejected_at',  'interview_at', 'short_letter', 'attachments', 'job']

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
        return_context = {}
        user = self.context['request'].user
        get_data = GetJobsSerializers(obj.job, context={"user": user})
        if get_data.data:
            return_context = get_data.data
        return return_context


class SavedJobSerializers(serializers.ModelSerializer):
    """Serializer class for serializing and deserializing SavedJob instances.

    This serializer class defines a ListField for attachments which allows files to be uploaded via a file input field.
    The attachments field is write-only and not required, but must not be null if present.

    Attributes:
        Meta (Meta): A nested class that defines metadata options for the serializer, including the model class and the
            fields to include in the serialized representation.

    Usage:
        To serialize an SavedJob instance, create an instance of this serializer and pass the instance to the data
        parameter.
    """

    class Meta:
        model = SavedJob
        fields = ['id', ]

    def save(self, user, job_instance):
        """Saves a new instance of the SavedJob model with the given user and job instance.

        Args:
            user (User): The user instance to associate with the job application.
            job_instance (Job): The job instance to associate with the job application.

        Returns:
            This instance of the SavedJobSerializers.

        Behavior:
            This method saves a new instance of the SavedJob model with the given user and job instance.

            The method returns the current instance of the serializer.

        Raises:
            Any exceptions raised during the save process.

        Usage:
            To create a new SavedJob instance and save attachments, call this method on an instance of
            SavedJobSerializers.

        """
        super().save(user=user, job=job_instance)
        return self


class GetSavedJobsSerializers(serializers.ModelSerializer):
    """
    A serializer class for the SavedJob model that returns details of saved jobs.

    This serializer includes the following fields:
        - id (int): The ID of the applied job.
        - job (dict): A dictionary containing details of the job posting.

    The 'job' field is a serialized representation of the related JobDetails object, and is populated
    using the `get_job` method of the GetSavedJobsSerializers class.
    """

    job = serializers.SerializerMethodField()

    class Meta:
        model = SavedJob
        fields = ['id', 'job']

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
        return_context = dict()
        try:
            if 'request' in self.context:
                user = self.context['request'].user
                get_data = GetJobsDetailSerializers(obj.job, context={"user": user})
                if get_data.data:
                    return_context = get_data.data
        except JobDetails.DoesNotExist:
            pass
        finally:
            return return_context


class UpdateJobPreferencesSerializers(serializers.ModelSerializer):
    """
        A serializer class for updating JobPreferences instances.

        This class extends the ModelSerializer class provided by Django REST framework, and specifies the
        `JobPreference`s model and a list of fields to include in the serialized representation.

        Attributes:
            - `Meta`: A class defining metadata options for the serializer, such as the model to serialize and the
            fields to include.
    """

    class Meta:
        model = JobPreferences
        fields = ['is_available', 'display_in_search', 'is_part_time',
                  'is_full_time', 'has_contract', 'expected_salary',
                  'pay_period'
                  ]

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        return instance


class GetAppliedJobsNotificationSerializers(serializers.ModelSerializer):
    """
    Serializer for the 'AppliedJob' model, used for generating notification data.

    This serializer is used to generate notification data for job applicants.
    It includes fields for the ID, shortlisted/rejected timestamps, cover letter, job object, user object,
    and attachments associated with an applied job.

    Serializer fields:
        - `id (int)`: The ID of the applied job.
        - `shortlisted_at (datetime)`: The timestamp of when the job was shortlisted.
        - `rejected_at (datetime)`: The timestamp of when the job was rejected.
        - `short_letter (str)`: The cover letter provided by the applicant.
        - `attachments (list)`: A list of attachment objects associated with the applied job.
        - `job (dict)`: A dictionary representing the job object associated with the applied job.
        - `user (dict)`: A dictionary representing the user object associated with the applied job.
    """

    user = serializers.SerializerMethodField()
    job = serializers.SerializerMethodField()
    attachments = serializers.SerializerMethodField()

    class Meta:
        model = AppliedJob
        fields = ['id', 'shortlisted_at', 'rejected_at', 'short_letter', 'attachments', 'job', 'user']

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
        Returns a dictionary representing the job associated with the given object.

        This method extracts information about the job associated with the given object,
        and returns a dictionary with keys for the job's ID and title.

        Args:
            obj: An object with a 'job' attribute that refers to a job object.

        Returns:
            A dictionary representing the job associated with the given object,
            with keys for the job's ID and title.
        """

        return {"id": obj.job.id, "title": obj.job.title}

    def get_user(self, obj):
        """
        Returns a dictionary representing the user associated with the given object.

        This method extracts information about the user associated with the given object,
        and returns a dictionary with keys for the user's ID, name, and image.

        Args:
            obj: An object with a 'user' attribute that refers to a user object.

        Returns:
            A dictionary representing the user associated with the given object,
            with keys for the user's ID, name, and image.
        """

        user = dict()
        user['id'] = obj.user.id
        user['name'] = obj.user.name
        user['email'] = obj.user.email
        if obj.user.image:
            if obj.user.image.title == "profile image":
                user['image'] = str(obj.user.image.file_path)
            else:
                user['image'] = obj.user.image.file_path.url
        return user


class AdditionalParameterSerializers(serializers.ModelSerializer):
    """
        A serializer for `JobSeekerProfile` instances with additional boolean fields.
        This serializer is used to serialize and deserialize `JobSeekerProfile` model instances with three additional
        boolean fields: is_part_time, is_full_time, and has_contract.

        Attributes:
        - `is_part_time (bool)`: A required boolean field indicating whether the job seeker is looking for part-time work.
        - `is_full_time (bool)`: A required boolean field indicating whether the job seeker is looking for full-time work.
        - `has_contract (bool)`: A required boolean field indicating whether the job seeker is looking for work with a
            contract.

        Methods:
        - `update(instance, validated_data)`: Overrides the default update method to update the associated `JobPreferences`
            model instance with the validated data.

    """

    is_part_time = serializers.BooleanField(
        required=True
    )
    is_full_time = serializers.BooleanField(
        required=True
    )
    has_contract = serializers.BooleanField(
        required=True
    )

    class Meta:
        model = JobSeekerProfile
        fields = ['country', 'city', 'is_part_time',
                  'is_full_time', 'has_contract'
                  ]

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        if JobPreferences.objects.filter(user=instance.user).exists():
            preference_instance = JobPreferences.objects.get(user=instance.user)
        else:
            preference_instance = JobPreferences.objects.create(user=instance.user)
        if 'is_part_time' in validated_data:
            preference_instance.is_part_time = validated_data['is_part_time']
        if 'is_full_time' in validated_data:
            preference_instance.is_full_time = validated_data['is_full_time']
        if 'has_contract' in validated_data:
            preference_instance.has_contract = validated_data['has_contract']
        preference_instance.save()
        return instance



class SubCategorySerializer(serializers.ModelSerializer):
    """
        Serializer for the sub-categories of a `JobSeekerCategory` model.
        Attributes:
            - `status (SerializerMethodField)`: A field that indicates whether the user has selected the `sub-category`.
        Meta:
            - `model (JobSeekerCategory)`: The model that the serializer is based on.
            - `fields (list)`: The fields to include in the serialized output.
        Methods:
            - `get_status`: A method that checks whether the user has selected the sub-category.
    """

    status = serializers.SerializerMethodField()

    class Meta:
        model = JobSubCategory
        fields = ['id', 'title', 'status']

    def get_status(self, obj):
        status = False
        if 'user' in self.context:
            user = self.context['user']
            if Categories.objects.filter(user=user, category=obj).exists():
                status = True
        return status

class CategoriesSerializers(serializers.ModelSerializer):
    """
        Serializer for the `JobSubCategory` model that includes its `sub-categories`.

        Attributes:
            - `sub_category (SerializerMethodField)`: A field that gets the `sub-categories` associated with the
                `category`.

        Meta:
            - `model (JobSubCategory)`: The model that the serializer is based on.
            - `fields (list)`: The fields to include in the serialized output.

        Methods:
            - `get_sub_category`: A method that retrieves the sub-categories associated with the category.
    """

    sub_category = serializers.SerializerMethodField()

    class Meta:
        model = JobCategory
        fields = ['id', 'title', 'sub_category']

    def get_sub_category(self, obj):
        context = []
        if 'user' in self.context:
            user = self.context['user']
            category_data = JobSubCategory.objects.filter(category=obj)
            get_data = SubCategorySerializer(category_data, many=True, context={'user': user})
            if get_data.data:
                context = get_data.data
        return context


class ModifyCategoriesSerializers(serializers.ModelSerializer):
    """
    Serializer for modifying the categories of a job seeker.

    Fields:
        - `category`: A list of category IDs to add or remove from the job seeker's existing categories.

    Methods:
        - `save(user)`: Saves the modified categories for the given user.
    """

    category = serializers.ListField(
        style={"input_type": "text"},
        write_only=True,
        allow_null=False,
        required=False
    )

    class Meta:
        model = Categories
        fields = ['id', 'category']

    def save(self, user):
        """
        Saves the modified categories for the given user.

        Args:
            - `user (User)`: The user object to modify categories for.

        Returns:
            - This serializer object.
        """

        category_list = None
        if 'category' in self.validated_data:
            category_list = self.validated_data.pop('category')
        if category_list:
            updated_categories = JobSubCategory.objects.filter(id__in=category_list)
            existing_jobseeker_categories = Categories.objects.filter(user=user).values('category')
            existing_categories = JobSubCategory.objects.filter(id__in=existing_jobseeker_categories)
            updated_qs = updated_categories.difference(existing_categories)
            Categories.objects.bulk_create([
                Categories(user=user, category=category) for category in updated_qs
            ])
            existing_jobseeker_categories = Categories.objects.filter(user=user).values('category')
            existing_categories = JobSubCategory.objects.filter(id__in=existing_jobseeker_categories)
            remove_jobseeker_categories = existing_categories.difference(updated_categories)
            for category in remove_jobseeker_categories:
                Categories.all_objects.filter(category=category, user=user).delete()
        else:
            Categories.all_objects.filter(user=user).delete()
        return self


class UpdateAppliedJobSerializers(serializers.ModelSerializer):
    """
    Serializer for updating an AppliedJob instance with attachments and attachment removal.

    This serializer is used to update an existing `AppliedJob instance` with new attachments or remove existing
    attachments. It provides the ability to upload multiple attachments as files, and also remove attachments by
    specifying their IDs. The serializer validates the data, updates the instance with the validated data, and
    handles attachments and attachment removal appropriately.

    Attributes:
        - `attachments (ListField)`: A list of file attachments to be added to the AppliedJob instance.
        - `attachments_remove (ListField)`: A list of attachment IDs to be removed from the AppliedJob instance.

    Meta:
        - `model (AppliedJob)`: The model to be used for the serializer.
        - `fields (list)`: The fields to be included in the serialized representation of the model.

    Methods:
        - `update(instance, validated_data)`: Update the instance with the validated data.

    Raises:
        N/A

    """

    attachments = serializers.ListField(
        style={"input_type": "file"},
        write_only=True,
        allow_null=False,
        required=False
    )
    attachments_remove = serializers.ListField(
        style={"input_type": "text"},
        write_only=True,
        allow_null=False,
        required=False
    )

    class Meta:
        model = AppliedJob
        fields = ['id', 'attachments', 'attachments_remove', 'short_letter']

    def update(self, instance, validated_data):
        attachments = None
        attachments_remove = None

        if 'attachments' in self.validated_data:
            attachments = self.validated_data.pop('attachments')
        if 'attachments_remove' in self.validated_data:
            attachments_remove = self.validated_data.pop('attachments_remove')

        applied_job_instance = super().update(instance, validated_data)
        if attachments_remove:
            for remove in attachments_remove:
                AppliedJobAttachmentsItem.objects.filter(id=remove).update(applied_job=None)

        if attachments:
            for attachment in attachments:
                content_type = str(attachment.content_type).split("/")
                if content_type[0] not in ["video", "image"]:
                    media_type = 'document'
                else:
                    media_type = content_type[0]
                # save media file into media table and get instance of saved data.
                media_instance = Media(title=attachment.name, file_path=attachment, media_type=media_type)
                media_instance.save()
                # save media instance into license id file into employer profile table.
                attachments_instance = AppliedJobAttachmentsItem.objects.create(applied_job=applied_job_instance,
                                                                                attachment=media_instance)
                attachments_instance.save()

        return instance
