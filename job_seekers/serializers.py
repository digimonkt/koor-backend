from rest_framework import serializers

from user_profile.models import JobSeekerProfile

from .models import (
    EducationRecord, JobSeekerLanguageProficiency, EmploymentRecord,
    JobSeekerSkill
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
                  'market_information_notification', 'job_notification', 
                  'full_name', 'email', 'mobile_number', 'country_code',
                  'highest_education'
                  ]
        
    
    def validate_mobile_number(self, mobile_number):
        if mobile_number != '':
            if mobile_number.isdigit():
                try:
                    if User.objects.get(mobile_number=mobile_number):
                        raise serializers.ValidationError('mobile_number already in use.', code='mobile_number')
                except User.DoesNotExist:
                    return mobile_number
            else:
                raise serializers.ValidationError('mobile_number must contain only numbers', code='mobile_number')
        else:
            raise serializers.ValidationError('mobile_number can not be blank', code='mobile_number')

    def validate_email(self, email):
        if email != '':
            email = email.lower()
            try:
                if User.objects.get(email=email):
                    raise serializers.ValidationError('email already in use.', code='email')
            except User.DoesNotExist:
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
    A serializer class for the `JobSeekerSkill` model to convert model instances into JSON serializable data and vice
    versa.

    Attributes: 
        - `Meta (inner class)`: Specifies the metadata for the serializer, including the model to use, and the fields
                                to include in the serialized data.

        - `model (JobSeekerSkill)`: The model class that the serializer should use.

        - `fields (list)`: The list of fields to include in the serialized data. 

    Returns: 
        Serialized data of the JobSeekerSkill model instance in `JSON format`. 
    """

    class Meta:
        model = JobSeekerSkill
        fields = ['id', 'skill']

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
