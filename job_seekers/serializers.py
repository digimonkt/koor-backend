from rest_framework import serializers

from user_profile.models import JobSeekerProfile

from jobs.models import JobDetails, JobAttachmentsItem
from employers.serializers import UserSerializer


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
    attachment = serializers.SerializerMethodField()

    class Meta:
        model = JobAttachmentsItem
        fields = (
            'attachment',
        )

    def get_attachment(self, obj):
        if obj.attachment:
            return obj.attachment.file_path.url
        return None


class GetJobsDetailSerializers(serializers.ModelSerializer):
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
        context = []
        attachments_data = JobAttachmentsItem.objects.filter(job=obj)
        get_data = AttachmentsSerializer(attachments_data, many=True)
        if get_data.data:
            context.append(get_data.data[0]['attachment'])
        return context
