from rest_framework import serializers

from project_meta.models import Media
from tenders.models import TenderDetails

from users.models import User
from user_profile.models import VendorProfile
from users.serializers import UserSerializer, ApplicantDetailSerializers

from tenders.serializers import (
    TendersDetailSerializers
)

from core.emails import get_email_object

from notification.models import Notification

from .models import (
    SavedTender, AppliedTenderAttachmentsItem, AppliedTender,
    VendorSector, VendorTag
)


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


class AppliedTenderAttachmentsSerializer(serializers.ModelSerializer):
    """
    Serializer for the AppliedTenderAttachmentsItem model.

    This serializer is used to serialize AppliedTenderAttachmentsItem objects to a JSON-compatible format, including
    a link to the attachment file if it exists.

    Attributes:
        attachment: A SerializerMethodField that calls the get_attachment method to retrieve the file path
            of the attachment.

    """
    title = serializers.SerializerMethodField()
    path = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = AppliedTenderAttachmentsItem
        fields = (
            'id', 'path', 'title', 'type'
        )

    def get_path(self, obj):
        """
        Retrieves the URL of the attachment file for a AppliedTenderAttachmentsItem object, if it exists.

        Args:
            obj: The AppliedTenderAttachmentsItem object to retrieve the attachment URL for.

        Returns:
            The URL of the attachment file if it exists, otherwise None.

        """
        if obj.attachment:
            return obj.attachment.file_path.url
        return None

    def get_title(self, obj):
        """
        Retrieves the URL of the attachment file for a AppliedTenderAttachmentsItem object, if it exists.

        Args:
            obj: The AppliedTenderAttachmentsItem object to retrieve the attachment URL for.

        Returns:
            The URL of the attachment file if it exists, otherwise None.

        """
        if obj.attachment:
            return obj.attachment.title
        return None

    def get_type(self, obj):
        """
        Retrieves the URL of the attachment file for a AppliedTenderAttachmentsItem object, if it exists.

        Args:
            obj: The AppliedTenderAttachmentsItem object to retrieve the attachment URL for.

        Returns:
            The URL of the attachment file if it exists, otherwise None.

        """
        if obj.attachment:
            return obj.attachment.media_type
        return None


class AppliedTenderSerializers(serializers.ModelSerializer):
    """Serializer class for serializing and deserializing AppliedTender instances.

    This serializer class defines a ListField for attachments which allows files to be uploaded via a file input field.
    The attachments field is write-only and not required, but must not be null if present.

    Attributes:
        attachments (ListField): A ListField instance with style "input_type": "file", write_only=True,
            allow_null=False, and required=False.
        Meta (Meta): A nested class that defines metadata options for the serializer, including the model class and the
            fields to include in the serialized representation.

    Usage:
        To serialize an AppliedTender instance, create an instance of this serializer and pass the instance to the data
        parameter.
    """

    attachments = serializers.ListField(
        style={"input_type": "file"},
        write_only=True,
        allow_null=False,
        required=False
    )

    class Meta:
        model = AppliedTender
        fields = ['id', 'attachments', 'short_letter']

    def save(self, user, tender_instace):
        """Saves a new instance of the AppliedTender model with the given user and tender instance, and saves any attachments
        to the tender application.

        Args:
            user (User): The user instance to associate with the tender application.
            tender_instance (TenderDetails): The tender instance to associate with the tender application.

        Returns:
            This instance of the AppliedTenderSerializers.

        Behavior:
            This method saves a new instance of the AppliedTender model with the given user and tender instance. If there are
            any attachments included in the validated data, each attachment is saved as a media instance and associated
            with the tender application by creating an AppliedTenderAttachmentsItem instance.

            The method returns the current instance of the serializer.

        Raises:
            Any exceptions raised during the save process.

        Usage:
            To create a new AppliedTender instance and save attachments, call this method on an instance of
            AppliedTenderSerializers.

        """

        attachments = None
        if 'attachments' in self.validated_data:
            attachments = self.validated_data.pop('attachments')
        applied_tender_instance = super().save(user=user, tender=tender_instace)
        Notification.objects.create(
            user=tender_instace.user, tender_application=applied_tender_instance,
            notification_type='applied_tender', created_by=user
        )
        if tender_instace.user.email:
            email_context = dict()
            if tender_instace.user.name:
                user_name = tender_instace.user.name
            else:
                user_name = tender_instace.user.email
            email_context["yourname"] = user_name
            email_context["notification_type"] = "applied tender"
            email_context["tender_instance"] = tender_instace
            if tender_instace.user.get_email:
                get_email_object(
                    subject=f'Notification for applied tender',
                    email_template_name='email-templates/send-notification.html',
                    context=email_context,
                    to_email=[tender_instace.user.email, ]
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
                attachments_instance = AppliedTenderAttachmentsItem.objects.create(applied_tender=applied_tender_instance,
                                                                                attachment=media_instance)
                attachments_instance.save()
        return self


class GetAppliedTenderSerializers(serializers.ModelSerializer):
    """
    A serializer class for the AppliedTender model that returns details of applied tenders.

    This serializer includes the following fields:
        - id (int): The ID of the applied tender.
        - shortlisted_at (datetime): The date and time when the tender was shortlisted.
        - rejected_at (datetime): The date and time when the tender was rejected.
        - short_letter (str): The short letter submitted with the tender application.
        - attachments (list): A list of URLs for any attachments submitted with the tender application.
        - tender (dict): A dictionary containing details of the tender posting.

    The 'tender' field is a serialized representation of the related JobDetails object, and is populated
    using the `get_tender` method of the GetAppliedTenderSerializers class.
    """

    tender = serializers.SerializerMethodField()
    attachments = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = AppliedTender
        fields = ['id', 'shortlisted_at', 'rejected_at', 'short_letter', 'attachments', 'tender', 'user']

    def get_attachments(self, obj):
        """Get the serialized attachment data for a AppliedTender object.

        This method uses the AppliedTenderAttachmentsItem model to retrieve the attachments associated with a AppliedTender
        object. It then uses the AppliedTenderAttachmentsSerializer to serialize the attachment data. If the serializer
        returns data, the first attachment in the list is extracted and added to a list, which is then returned.

        Args:
            obj: A AppliedTender object whose attachment data will be serialized.

        Returns:
            A list containing the first serialized attachment data, or an empty list if the serializer did
            not return any data.

        """

        context = []
        attachments_data = AppliedTenderAttachmentsItem.objects.filter(applied_tender=obj)
        get_data = AppliedTenderAttachmentsSerializer(attachments_data, many=True)
        if get_data.data:
            context = get_data.data
        return context

    def get_tender(self, obj):
        """
        Returns a dictionary with details of a tender posting.

        Args:
            obj: An object representing a tender application.

        Returns:
            A dictionary containing details of the tender posting, such as the tender title, company name,
            tender location, etc.

        If the tender posting does not exist, an empty dictionary will be returned.
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

    def get_user(self, obj):
        """Get the serialized user data for a AppliedTender object.

        This method uses the UserSerializer to serialize the users associated with a AppliedTender
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A AppliedTender object whose user data will be serialized.

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


class UpdateAppliedTenderSerializers(serializers.ModelSerializer):
    """
    Serializer for updating an AppliedTender instance with attachments and attachment removal.

    This serializer is used to update an existing `AppliedTender instance` with new attachments or remove existing
    attachments. It provides the ability to upload multiple attachments as files, and also remove attachments by
    specifying their IDs. The serializer validates the data, updates the instance with the validated data, and
    handles attachments and attachment removal appropriately.

    Attributes:
        - `attachments (ListField)`: A list of file attachments to be added to the AppliedTender instance.
        - `attachments_remove (ListField)`: A list of attachment IDs to be removed from the AppliedTender instance.

    Meta:
        - `model (AppliedTender)`: The model to be used for the serializer.
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
        model = AppliedTender
        fields = ['id', 'attachments', 'attachments_remove', 'short_letter']

    def update(self, instance, validated_data):
        attachments = None
        attachments_remove = None

        if 'attachments' in self.validated_data:
            attachments = self.validated_data.pop('attachments')
        if 'attachments_remove' in self.validated_data:
            attachments_remove = self.validated_data.pop('attachments_remove')

        applied_tender_instance = super().update(instance, validated_data)
        if attachments_remove:
            for remove in attachments_remove:
                AppliedTenderAttachmentsItem.objects.filter(id=remove).update(applied_tender=None)

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
                attachments_instance = AppliedTenderAttachmentsItem.objects.create(applied_tender=applied_tender_instance,
                                                                                attachment=media_instance)
                attachments_instance.save()

        return instance


class GetAppliedTenderApplicationSerializers(serializers.ModelSerializer):
    """
    A serializer class for the AppliedTender model that returns details of applied tenders.

    This serializer includes the following fields:
        - id (int): The ID of the applied tender.
        - shortlisted_at (datetime): The date and time when the tender was shortlisted.
        - rejected_at (datetime): The date and time when the tender was rejected.
        - short_letter (str): The short letter submitted with the tender application.
        - attachments (list): A list of URLs for any attachments submitted with the tender application.
        - tender (dict): A dictionary containing details of the tender posting.

    The 'tender' field is a serialized representation of the related JobDetails object, and is populated
    using the `get_tender` method of the GetAppliedTenderSerializers class.
    """

    tender = serializers.SerializerMethodField()
    attachments = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = AppliedTender
        fields = ['id', 'shortlisted_at', 'rejected_at', 'short_letter', 'attachments', 'tender', 'user']

    def get_attachments(self, obj):
        """Get the serialized attachment data for a AppliedTender object.

        This method uses the AppliedTenderAttachmentsItem model to retrieve the attachments associated with a AppliedTender
        object. It then uses the AppliedTenderAttachmentsSerializer to serialize the attachment data. If the serializer
        returns data, the first attachment in the list is extracted and added to a list, which is then returned.

        Args:
            obj: A AppliedTender object whose attachment data will be serialized.

        Returns:
            A list containing the first serialized attachment data, or an empty list if the serializer did
            not return any data.

        """

        context = []
        attachments_data = AppliedTenderAttachmentsItem.objects.filter(applied_tender=obj)
        get_data = AppliedTenderAttachmentsSerializer(attachments_data, many=True)
        if get_data.data:
            context = get_data.data
        return context

    def get_tender(self, obj):
        """
        Returns a dictionary with details of a tender posting.

        Args:
            obj: An object representing a tender application.

        Returns:
            A dictionary containing details of the tender posting, such as the tender title, company name,
            tender location, etc.

        If the tender posting does not exist, an empty dictionary will be returned.
        """
        return {'id': obj.tender.id, 'title': obj.tender.title}

    def get_user(self, obj):
        """Get the serialized user data for a AppliedTender object.

        This method uses the UserSerializer to serialize the users associated with a AppliedTender
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A AppliedTender object whose user data will be serialized.

        Returns:
            A dictionary containing the serialized user data, or an empty dictionary if the
            serializer did not return any data.

        """

        context = {}
        if obj.user:
            get_data = ApplicantDetailSerializers(obj.user)
            if get_data.data:
                context = get_data.data
        return context
    

class VendorSectorSerializers(serializers.ModelSerializer):
    """
    Serializes and validates the 'VendorSector' model with the specified fields.

    Attributes:
        sector_add (List): A list of sectors to add.
        sector_remove (List): A list of sectors to remove.

    Meta:
        model (class): The model class to be serialized.
        fields (list): The fields to be included in the serialization.

    Methods:
        validate(self, data): Validates the input data and performs sector removal if necessary.
    """

    sector_add = serializers.ListField(
        style={"input_type": "text"},
        write_only=True,
        allow_null=False
    )
    sector_remove = serializers.ListField(
        style={"input_type": "text"},
        write_only=True,
        allow_null=False
    )

    class Meta:
        model = VendorSector
        fields = ['id', 'sector_remove', 'sector_add']

    def validate(self, data):
        sector_add = data.get("sector_add")
        sector_remove = data.get("sector_remove")
        if sector_remove:
            for remove in sector_remove:
                VendorSector.objects.filter(id=remove).delete()
        return sector_add


class VendorTagSerializers(serializers.ModelSerializer):
    """
    Serializes and validates the 'VendorTag' model with the specified fields.

    Attributes:
        tag_add (List): A list of tags to add.
        tag_remove (List): A list of tags to remove.

    Meta:
        model (class): The model class to be serialized.
        fields (list): The fields to be included in the serialization.

    Methods:
        validate(self, data): Validates the input data and performs tag removal if necessary.
    """

    tag_add = serializers.ListField(
        style={"input_type": "text"},
        write_only=True,
        allow_null=False
    )
    tag_remove = serializers.ListField(
        style={"input_type": "text"},
        write_only=True,
        allow_null=False
    )

    class Meta:
        model = VendorTag
        fields = ['id', 'tag_remove', 'tag_add']

    def validate(self, data):
        tag_add = data.get("tag_add")
        tag_remove = data.get("tag_remove")
        if tag_remove:
            for remove in tag_remove:
                VendorTag.objects.filter(id=remove).delete()
        return tag_add
