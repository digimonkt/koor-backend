from rest_framework import serializers

from tenders.models import (
    TenderDetails, TenderCategory,
    TenderAttachmentsItem, TenderFilter
)

from users.serializers import UserSerializer

from project_meta.serializers import (
    CitySerializer, CountrySerializer,
    TagSerializer
)


class TenderCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the TenderCategory model.

    This serializer is used to serialize/deserialize TenderCategory objects to/from JSON format. It defines
    the fields that will be included in the serialized data and provides validation for deserialization.

    Attributes:
        Meta: A subclass of the serializer that specifies the model to be serialized and the fields
            to be included in the serialized data.
    """

    class Meta:
        model = TenderCategory
        fields = (
            'id',
            'title'
        )


class TendersSerializers(serializers.ModelSerializer):
    """
    Serializer for the `TenderDetails` model.

    Attributes:
        - `tender_category (SerializerMethodField)`: A read-only field that returns the serialized representation of
            the `tender's category`.
        - `user (SerializerMethodField)`: A read-only field that returns the serialized representation of the
            `tender's user`.
        - `is_applied (SerializerMethodField)`: A read-only field that returns a boolean indicating whether
            the authenticated user has applied for the tender.
        - `is_saved (SerializerMethodField)`: A read-only field that returns a boolean indicating whether
            the authenticated user has saved the tender.

    """

    tender_category = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    is_applied = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    vendor = serializers.SerializerMethodField()

    class Meta:
        model = TenderDetails
        fields = [
            'id', 'title', 'description', 'tender_category', 'sector',
            'created', 'is_applied', 'is_saved', 'user', 'vendor',
            'status'
        ]

    def get_tender_category(self, obj):
        """
        Retrieves the serialized data for the tender category related to a TenderDetails object.

        Args:
            obj: The TenderDetails object to retrieve the tender category data for.

        Returns:
            A dictionary containing the serialized tender category data.

        """

        context = {}
        get_data = TenderCategorySerializer(obj.tender_category, many=True)
        if get_data.data:
            context = get_data.data
        return context

    def get_user(self, obj):
        """
        Retrieves the serialized data for the user related to a TenderDetails object.

        Args:
            obj: The TenderDetails object to retrieve the user data for.

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
            # if user.is_authenticated:
            #     is_applied_record = AppliedJob.objects.filter(
            #         job=obj,
            #         user=user
            #     ).exists()
        return is_applied_record

    def get_is_saved(self, obj):
        is_saved_record = False
        # if 'user' in self.context:
        #     if self.context['user'].is_authenticated:
        #         is_saved_record = SavedJob.objects.filter(
        #             job=obj,
        #             user=self.context['user']
        #         ).exists()
        return is_saved_record

    def get_vendor(self, obj):
        return 0


class TenderAttachmentsSerializer(serializers.ModelSerializer):
    """
    Serializer for the TenderAttachmentsItem model.

    This serializer is used to serialize TenderAttachmentsItem objects to a JSON-compatible format, including
    a link to the attachment file if it exists.

    Attributes:
        attachment: A SerializerMethodField that calls the get_attachment method to retrieve the file path
            of the attachment.

    """
    title = serializers.SerializerMethodField()
    path = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = TenderAttachmentsItem
        fields = (
            'id', 'path', 'title', 'type'
        )

    def get_path(self, obj):
        """
        Retrieves the URL of the attachment file for a TenderAttachmentsItem object, if it exists.

        Args:
            obj: The TenderAttachmentsItem object to retrieve the attachment URL for.

        Returns:
            The URL of the attachment file if it exists, otherwise None.

        """
        if obj.attachment:
            return obj.attachment.file_path.url
        return None

    def get_title(self, obj):
        """
        Retrieves the URL of the attachment file for a TenderAttachmentsItem object, if it exists.

        Args:
            obj: The TenderAttachmentsItem object to retrieve the attachment URL for.

        Returns:
            The URL of the attachment file if it exists, otherwise None.

        """
        if obj.attachment:
            return obj.attachment.title
        return None

    def get_type(self, obj):
        """
        Retrieves the URL of the attachment file for a TenderAttachmentsItem object, if it exists.

        Args:
            obj: The TenderAttachmentsItem object to retrieve the attachment URL for.

        Returns:
            The URL of the attachment file if it exists, otherwise None.

        """
        if obj.attachment:
            return obj.attachment.media_type
        return None


class TendersDetailSerializers(serializers.ModelSerializer):
    """
    A serializer class to serialize the fields of a `TenderDetails` object.

    This serializer uses different serializers to serialize various fields of a `TenderDetails` object such as
    `country`, `city`, `tender category`, `tag`, `user`, `vendor`, `attachments`, etc.

    Attributes:
        - `country`: A SerializerMethodField to serialize the `country field` of a TenderDetails object.
        - `city`: A SerializerMethodField to serialize the `city field` of a TenderDetails object.
        - `tender_category`: A SerializerMethodField to serialize the `tender category field` of a TenderDetails object.
        - `tag`: A SerializerMethodField to serialize the `tag field` of a TenderDetails object.
        - `user`: A SerializerMethodField to serialize the `user field` of a TenderDetails object.
        - `vendor`: A SerializerMethodField to serialize the `vendor field` of a TenderDetails object.
        - `is_applied`: A SerializerMethodField to serialize the `is_applied field` of a TenderDetails object.
        - `is_saved`: A SerializerMethodField to serialize the `is_saved field` of a TenderDetails object.
        - `attachments`: A SerializerMethodField to serialize the `attachments field` of a TenderDetails object.

    Methods:
        - `get_country(obj)`: Get the serialized `country data` for a TenderDetails object.
        - `get_city(obj)`: Get the serialized `city data` for a TenderDetails object.
        - `get_tender_category(obj)`: Get the serialized `tender category data` for a TenderDetails object.
        - `get_tag(obj)`: Get the serialized `tag data` for a TenderDetails object.
        - `get_user(obj)`: Get the serialized `user data` for a TenderDetails object.
        - `get_vendor(obj)`: Get the number of `vendors associated with` a TenderDetails object.
        - `get_is_applied(obj)`: Get whether the current `user has applied` to the TenderDetails object.
        - `get_is_saved(obj)`: Get whether the current `user has saved` the TenderDetails object.
        - `get_attachments(obj)`: Get the serialized `attachment data` for a TenderDetails object.

    """

    country = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    tender_category = serializers.SerializerMethodField()
    tag = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    vendor = serializers.SerializerMethodField()
    is_applied = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    attachments = serializers.SerializerMethodField()

    class Meta:
        model = TenderDetails
        fields = [
            'id', 'title', 'tender_id', 'budget_currency', 'budget_amount', 'description',
            'country', 'city', 'tag', 'tender_category', 'tender_type', 'sector', 'deadline',
            'start_date', 'status', 'user', 'attachments', 'created', 'vendor',
            'is_applied', 'is_saved'

        ]

    def get_country(self, obj):
        """Get the serialized country data for a TenderDetails object.

        This method uses the CountrySerializer to serialize the country associated with a TenderDetails
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A TenderDetails object whose country data will be serialized.

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
        """Get the serialized city data for a TenderDetails object.

        This method uses the CitySerializer to serialize the city associated with a TenderDetails
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A TenderDetails object whose city data will be serialized.

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

    def get_tender_category(self, obj):
        """Get the serialized tender category data for a TenderDetails object.

        This method uses the TenderCategorySerializer to serialize the tender categories associated with a TenderDetails
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A TenderDetails object whose tender category data will be serialized.

        Returns:
            A dictionary containing the serialized tender category data, or an empty dictionary if the
            serializer did not return any data.

        """

        context = []
        get_data = TenderCategorySerializer(obj.tender_category, many=True)
        if get_data.data:
            context = get_data.data
        return context

    def get_tag(self, obj):
        """
        Get the serialized tag data for a TenderDetails object.

        This method uses the TagSerializer to serialize the tender categories associated with a TenderDetails
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A TenderDetails object whose tag data will be serialized.

        Returns:
            A dictionary containing the serialized tag data, or an empty dictionary if the
            serializer did not return any data.

        """

        context = []
        get_data = TagSerializer(obj.tag, many=True)
        if get_data.data:
            context = get_data.data
        return context

    def get_user(self, obj):
        """Get the serialized user data for a TenderDetails object.

        This method uses the UserSerializer to serialize the users associated with a TenderDetails
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A TenderDetails object whose user data will be serialized.

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

    def get_vendor(self, obj):
        # return AppliedJob.objects.filter(job=obj).count()
        return 0

    def get_is_applied(self, obj):
        is_applied_record = False
        # if 'user' in self.context:
        #     user = self.context['user']
        #     is_applied_record = AppliedJob.objects.filter(
        #         job=obj,
        #         user=user
        #     ).exists()
        return is_applied_record

    def get_is_saved(self, obj):
        is_saved_record = False
        # if 'user' in self.context:
        #     user = self.context['user']
        #     is_saved_record = SavedJob.objects.filter(
        #         job=obj,
        #         user=user
        #     ).exists()
        return is_saved_record

    def get_attachments(self, obj):
        """Get the serialized attachment data for a TenderDetails object.

        This method uses the TenderAttachmentsItem model to retrieve the attachments associated with a TenderDetails
        object. It then uses the AttachmentsSerializer to serialize the attachment data. If the serializer
        returns data, the first attachment in the list is extracted and added to a list, which is then returned.

        Args:
            obj: A TenderDetails object whose attachment data will be serialized.

        Returns:
            A list containing the first serialized attachment data, or an empty list if the serializer did
            not return any data.

        """

        context = []
        attachments_data = TenderAttachmentsItem.objects.filter(tender=obj)
        get_data = TenderAttachmentsSerializer(attachments_data, many=True)
        if get_data.data:
            context = get_data.data
        return context


class TenderFiltersSerializers(serializers.ModelSerializer):
    """
    TenderFiltersSerializers is a class-based serializer that inherits from the ModelSerializer class of the Django REST
    Framework.
    It defines a Meta class that specifies the TenderFilter model and the fields to be included in the serialization.

    Attributes:
        - `model (class)`: The Django model class that this serializer is based on.
        - `fields (list)`: A list of fields to be included in the serialized output.
        
    Usage:
        - This serializer can be used to serialize TenderFilter objects and convert them to JSON format for use in HTTP
        requests and responses.
    """

    class Meta:
        model = TenderFilter
        fields = [
            'id', 'title', 'country', 'city', 'opportunity_type',
            'sector', 'deadline', 'budget', 'tender_category', 'tag',
            'is_notification'
        ]

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        return instance
