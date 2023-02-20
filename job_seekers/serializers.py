from rest_framework import serializers

from jobs.models import JobDetails
from project_meta.models import Media
from user_profile.models import JobSeekerProfile

from jobs.serializers import GetJobsDetailSerializers

from .models import (
    EducationRecord, JobSeekerLanguageProficiency, EmploymentRecord,
    JobSeekerSkill, AppliedJob, AppliedJobAttachmentsItem
)


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
    email = serializers.CharField(
        style={"input_type": "text"},
        write_only=True,
        allow_blank=False
    )
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
                  'full_name', 'email', 'mobile_number', 'country_code',
                  'highest_education'
                  ]

    def validate_mobile_number(self, mobile_number):
        if mobile_number != '':
            if mobile_number.isdigit():
                return mobile_number
            else:
                raise serializers.ValidationError('mobile_number must contain only numbers', code='mobile_number')
        else:
            raise serializers.ValidationError('mobile_number can not be blank', code='mobile_number')

    def validate_email(self, email):
        if email != '':
            email = email.lower()
            return email
        else:
            raise serializers.ValidationError('email can not be blank', code='email')

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
        if 'email' in validated_data:
            instance.user.email = validated_data['email']
            instance.user.save()
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
                JobSeekerSkill.objects.filter(skill=remove).delete()
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

    def save(self, user, job_instace):
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
        applied_job_instance = super().save(user=user, job=job_instace)
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
        fields = ['id', 'shortlisted_at', 'rejected_at', 'short_letter', 'attachments', 'job']

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

        context = dict()
        try:
            get_data = GetJobsDetailSerializers(obj.job)
            if get_data.data:
                context = get_data.data
        except JobDetails.DoesNotExist:
            pass
        finally:
            return context
