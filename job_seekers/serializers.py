from rest_framework import serializers

from user_profile.models import JobSeekerProfile

from jobs.models import JobDetails, JobAttachmentsItem
from employers.serializers import UserSerializer

from .models import (
    EducationRecord
)


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

    class Meta:
        model = JobSeekerProfile
        fields = ['gender', 'dob', 'employment_status', 'description',
                  'market_information_notification', 'job_notification', 'full_name']

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        if 'full_name' in validated_data:
            instance.user.name = validated_data['full_name']
            instance.user.save()
        return instance


class AttachmentsSerializer(serializers.ModelSerializer):
    """
    Serializer class to retrieve job attachment data.

    This serializer class is used to retrieve job attachment data, such as the attachment URL and media type.

    Attributes:
        - `attachment`: A SerializerMethodField that retrieves the attachment URL from the related Attachment model.
        - `file_type`: A SerializerMethodField that retrieves the media type from the related Attachment model.

    Meta:
        - `model`: The model to be serialized, which is JobAttachmentsItem.
        - `fields`: A tuple of fields to be included in the serialized output.

    Methods:
        - `get_attachment`: A method that retrieves the attachment URL from the related Attachment model.
        - `get_file_type`: A method that retrieves the media type from the related Attachment model.
    """
    attachment = serializers.SerializerMethodField()
    file_type = serializers.SerializerMethodField()

    class Meta:
        model = JobAttachmentsItem
        fields = (
            'id',
            'attachment',
            'file_type'
        )

    def get_attachment(self, obj):
        if obj.attachment:
            return obj.attachment.file_path.url
        return None

    def get_file_type(self, obj):
        if obj.attachment:
            return obj.attachment.media_type
        return None


class GetJobsDetailSerializers(serializers.ModelSerializer):
    """Serializer class to retrieve job details with related data.

    This serializer class is used to retrieve job details along with related data, such as country and city names,
    user information, attachments, and more.

    Attributes:
        - `country`: A SerializerMethodField that retrieves the country name from the related Country model.
        - `city`: A SerializerMethodField that retrieves the city name from the related City model.
        - `user`: A SerializerMethodField that retrieves the user information from the related User model.
        - `applicant`: A SerializerMethodField that returns a default value of 0.
        - `attachments`: A SerializerMethodField that retrieves the attachments data from the related JobAttachmentsItem
        model.

    Meta:
        - `model`: The model to be serialized, which is JobDetails.
        - `fields`: A list of fields to be included in the serialized output.

    Methods:
        - `get_country`: A method that retrieves the country name from the related Country model.
        - `get_city`: A method that retrieves the city name from the related City model.
        - `get_user`: A method that retrieves the user information from the related User model.
        - `get_applicant`: A method that returns a default value of 0.
        - `get_attachments`: A method that retrieves the attachments data from the related JobAttachmentsItem model.
    """
    country = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    applicant = serializers.SerializerMethodField()
    attachments = serializers.SerializerMethodField()

    class Meta:
        model = JobDetails
        fields = [
            'id', 'title', 'description', 'budget_currency', 'budget_amount', 'budget_pay_period',
            'country', 'city', 'address', 'job_category', 'is_full_time', 'is_part_time', 'has_contract',
            'contact_email', 'contact_phone', 'contact_whatsapp', 'highest_education', 'language', 'skill',
            'working_days', 'status', 'applicant', 'created', 'user', 'attachments'

        ]

    def get_country(self, obj):
        return obj.country.title

    def get_city(self, obj):
        return obj.city.title

    def get_user(self, obj):
        context = {}
        get_data = UserSerializer(obj.user)
        if get_data.data:
            context = get_data.data
        return context

    def get_applicant(self, obj):
        return 0

    def get_attachments(self, obj):
        context = dict()
        attachments_data = JobAttachmentsItem.objects.filter(job=obj)
        get_data = AttachmentsSerializer(attachments_data, many=True)
        if get_data.data:
            context = get_data.data
        return context


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
        fields = ['id', 'title', 'start_date', 'end_date', 'institute', 'description']
