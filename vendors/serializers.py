from rest_framework import serializers

from project_meta.models import Media
from tenders.models import TenderDetails

from users.models import User
from user_profile.models import VendorProfile

from tenders.serializers import (
    TendersDetailSerializers
)

from .models import SavedTender


class UpdateAboutSerializers(serializers.ModelSerializer):
    """
    A `ModelSerializer` to update the fields of a `VendorProfile` instance.

    This serializer accepts the following fields:
        - `organization_name (required CharField)`: the name of the organization.
        - `license (required FileField)`: the uploaded license file.
        - `organization_type (CharField)`: the type of the organization.
        - `license_id (CharField)`: the ID of the uploaded license.
        - `registration_number (CharField)`: the registration number of the organization.
        - `registration_certificate (FileField)`: the uploaded registration certificate file.
        - `market_information_notification (BooleanField)`: whether to receive market information notifications.
        - `other_notification (BooleanField)`: whether to receive other notifications.
        - `operating_years (IntegerField)`: the number of years the organization has been operating.
        - `jobs_experience (CharField)`: the organization's experience in jobs.

    This serializer also provides validation for the `license_id` and `registration_number` fields.
    Upon successful update, the serializer saves the `organization_name` field to the corresponding User instance.
    It also saves the uploaded `license` and `registration_certificate` files as Media instances and updates
    the corresponding fields in the `VendorProfile instance`.

    """

    organization_name = serializers.CharField(
        style={"input_type": "text"},
        write_only=True,
        allow_blank=False
    )
    license = serializers.FileField(
        style={"input_type": "file"},
        write_only=True,
        allow_null=False
    )
    certificate = serializers.FileField(
        style={"input_type": "file"},
        write_only=True,
        allow_null=False
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
        model = VendorProfile
        fields = [
            'organization_name', 'organization_type', 'license_id',
            'license', 'registration_number', 'certificate',
            'market_information_notification', 'other_notification',
            'operating_years', 'jobs_experience', 'description',
            'website', 'mobile_number', 'country_code', 'address',
            'country', 'city',
        ]

    def validate_license_id(self, license_id):
        """
        A validation method for the `license_id` field.

        Raises a `serializers.ValidationError` if the field is empty.

        Parameters:
            - `license_id (str)`: the value of the `license_id` field.

        Returns:
            - `license_id (str)`: the validated `license_id` field.

        """

        if license_id == '':
            raise serializers.ValidationError('License id can not be blank.', code='license_id')
        else:
            return license_id

    def validate_registration_number(self, registration_number):
        """
        A validation method for the `registration_number` field.

        Raises a `serializers.ValidationError` if the field is empty.

        Parameters:
            - `registration_number (str)`: the value of the `registration_number` field.

        Returns:
            - `registration_number (str)`: the validated `registration_number` field.

        """

        if registration_number == '':
            raise serializers.ValidationError('Registration number can not be blank.', code='registration_number')
        else:
            return registration_number

    def validate_mobile_number(self, mobile_number):
        if mobile_number != '':
            if mobile_number.isdigit():
                if len(mobile_number) > 13:
                    raise serializers.ValidationError('This is an invalid mobile number.', code='mobile_number')
                else:
                    return mobile_number
            else:
                raise serializers.ValidationError('Mobile number must contain only numbers', code='mobile_number')
        else:
            raise serializers.ValidationError('Mobile number can not be blank', code='mobile_number')

    def update(self, instance, validated_data):
        """
        Updates the fields of a `VendorProfile` instance.

        Upon successful update, saves the `organization_name` field to the corresponding User instance.
        It also saves the uploaded `license` and `registration_certificate` files as Media instances and updates
        the corresponding fields in the VendorProfile instance.

        Parameters:
            - `instance (VendorProfile)`: the instance of the `VendorProfile` to be updated.
            - `validated_data (dict)`: the validated data to be updated.

        Returns:
            - `instance (VendorProfile)`: the updated instance of the `VendorProfile`.

        """

        super().update(instance, validated_data)
        if 'organization_name' in validated_data:
            instance.user.name = validated_data['organization_name']
            instance.user.save()
        if 'mobile_number' in validated_data:
            instance.user.mobile_number = validated_data['mobile_number']
            instance.user.country_code = validated_data['country_code']
            instance.user.save()
        if 'license' in validated_data:
            # Get media type from upload license file
            content_type = str(validated_data['license'].content_type).split("/")
            if content_type[0] not in ["video", "image"]:
                media_type = 'document'
            else:
                media_type = content_type[0]
            # save media file into media table and get instance of saved data.
            media_instance = Media(title=validated_data['license'].name, 
                                   file_path=validated_data['license'],
                                   media_type=media_type)
            media_instance.save()
            # save media instance into license id file into employer profile table.
            instance.license_id_file = media_instance
            instance.save()
        if 'certificate' in validated_data:
            # Get media type from upload license file
            content_type = str(validated_data['certificate'].content_type).split("/")
            if content_type[0] not in ["video", "image"]:
                media_type = 'document'
            else:
                media_type = content_type[0]
            # save media file into media table and get instance of saved data.
            media_instance = Media(
                title=validated_data['certificate'].name,
                file_path=validated_data['certificate'],
                media_type=media_type
            )
            media_instance.save()
            # save media instance into registration certificate into vendor table.
            instance.registration_certificate = media_instance
            instance.save()
        return instance


class SavedTenderSerializers(serializers.ModelSerializer):
    """
    Serializer for the `SavedTender` model, which extends the `ModelSerializer` class.
    It serializes the 'id' field of a `SavedTender` instance and defines a custom '`save`' method to create a new
    `SavedTender` instance with the specified user and tender instance.

    Attributes:
        - `Meta (class)`: defines the model to be serialized and the fields to include in the serializer.

    Methods:
        - `save(user, tender_instace)`: creates and saves a new `SavedTender` instance with the specified user and
        ``tender instance`.
            - `Args`:
                - `user (User)`: the user who saved the tender.
                - `tender_instace (Tender)`: the tender instance that was saved.
            - `Returns:
                - `self (SavedTenderSerializers)`: the instance of the `SavedTenderSerializers` class.
    """

    class Meta:
        model = SavedTender
        fields = ['id', ]

    def save(self, user, tender_instace):

        super().save(user=user, tender=tender_instace)
        return self


class GetSavedTenderSerializers(serializers.ModelSerializer):
    """
    A serializer class for the SavedTender model that returns details of saved tenders.

    This serializer includes the following fields:
        - id (int): The ID of the applied tender.
        - tender (dict): A dictionary containing details of the tender posting.

    The 'tender' field is a serialized representation of the related TenderDetails object, and is populated
    using the `get_tender` method of the GetSavedTenderSerializers class.
    """

    tender = serializers.SerializerMethodField()

    class Meta:
        model = SavedTender
        fields = ['id', 'tender']

    def get_tender(self, obj):
        """
        A method for retrieving the details of a tender.

        - `obj`: An instance of a model that has a related TenderDetails object.
        - `return_context`: A dictionary that contains the serialized data of the related tender details.

        The method attempts to retrieve the serialized data of the related tender details object by:
            - Checking if a 'request' object is present in the context.
            - Retrieving the authenticated user from the '`request`' object.
            - Serializing the tender details object using the `TendersDetailSerializers` and passing the authenticated
                user as context.
            - Checking if the serialized data is `not empty`.
            - If the above steps are successful, the serialized data is returned as a dictionary.
        If the TenderDetails object does not exist, an exception is caught and nothing is returned.

        """

        return_context = dict()
        try:
            if 'request' in self.context:
                user = self.context['request'].user
                get_data = TendersDetailSerializers(obj.tender, context={"user": user})
                if get_data.data:
                    return_context = get_data.data
        except TenderDetails.DoesNotExist:
            pass
        finally:
            return return_context
