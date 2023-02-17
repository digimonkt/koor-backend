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
