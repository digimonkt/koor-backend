from rest_framework import serializers
from datetime import date

from tenders.models import (
    TenderDetails, TenderCategory,
    TenderAttachmentsItem, TenderFilter
)

from vendors.models import (
    SavedTender, AppliedTender
)

from users.serializers import UserSerializer

from project_meta.serializers import (
    CitySerializer, CountrySerializer,
    TagSerializer, ChoiceSerializer,
    OpportunityTypeSerializer
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
    sector = serializers.SerializerMethodField()
    company_logo = serializers.SerializerMethodField()

    class Meta:
        model = TenderDetails
        fields = [
            'id', 'title', 'description', 'tender_category', 'sector',
            'created', 'deadline','start_date', 'is_applied', 'is_saved', 'user', 'vendor',
            'status', 'address', 'company', 'company_logo', 'post_by_admin', 'slug'
        ]
        
    def get_company_logo(self, obj):
        if obj.company_logo:
            return {'id':str(obj.company_logo.id), 'path':obj.company_logo.file_path.url}
        return None

    def get_tender_category(self, obj):
        """
        Retrieves the serialized data for the tender category related to a TenderDetails object.

        Args:
            obj: The TenderDetails object to retrieve the tender category data for.

        Returns:
            A dictionary containing the serialized tender category data.

        """

        context = []
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
            if user.is_authenticated:
                is_applied_record = AppliedTender.objects.filter(
                    tender=obj,
                    user=user
                ).exists()
        return is_applied_record

    def get_is_saved(self, obj):
        is_saved_record = False
        if 'user' in self.context:
            if self.context['user'].is_authenticated:
                is_saved_record = SavedTender.objects.filter(
                    tender=obj,
                    user=self.context['user']
                ).exists()
        return is_saved_record

    def get_vendor(self, obj):
        return AppliedTender.objects.filter(tender=obj).count()

    def get_sector(self, obj):
        """
        Retrieves the serialized data for the organization type related to a JobDetails object.

        Args:
            obj: The JobDetails object to retrieve the organization type data for.

        Returns:
            A dictionary containing the serialized organization type data.

        """

        context = {}
        if obj.sector:
            get_data = ChoiceSerializer(obj.sector, many=True)
            if get_data.data:
                context = get_data.data[0]
        return context


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
    sector = serializers.SerializerMethodField()
    tender_type = serializers.SerializerMethodField()
    is_editable = serializers.SerializerMethodField()
    application = serializers.SerializerMethodField()
    company_logo = serializers.SerializerMethodField()

    class Meta:
        model = TenderDetails
        fields = [
            'id', 'title', 'tender_id', 'budget_currency', 'budget_amount', 'description',
            'country', 'city', 'tag', 'tender_category', 'tender_type', 'sector', 'deadline',
            'start_date', 'status', 'user', 'attachments', 'created', 'vendor',
            'is_applied', 'is_saved', 'is_editable', 'application', 'address', 'company', 'company_logo',
            'contact_email', 'cc1', 'cc2', 'contact_whatsapp', 'apply_through_koor', 
            'apply_through_email', 'apply_through_website', 'application_instruction', 
            'website_link', 'slug'

        ]
    def get_company_logo(self, obj):
        if obj.company_logo:
            return {'id':str(obj.company_logo.id), 'path':obj.company_logo.file_path.url}
        return None
    
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
        return AppliedTender.objects.filter(tender=obj).count()

    def get_is_applied(self, obj):
        is_applied_record = False
        if 'user' in self.context:
            user = self.context['user']
            is_applied_record = AppliedTender.objects.filter(
                tender=obj,
                user=user
            ).exists()
        return is_applied_record

    def get_is_saved(self, obj):
        is_saved_record = False
        if 'user' in self.context:
            user = self.context['user']
            is_saved_record = SavedTender.objects.filter(
                tender=obj,
                user=user
            ).exists()
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

    def get_sector(self, obj):
        """
        Retrieves the serialized data for the organization type related to a JobDetails object.

        Args:
            obj: The JobDetails object to retrieve the organization type data for.

        Returns:
            A dictionary containing the serialized organization type data.

        """

        context = {}
        if obj.sector:
            get_data = ChoiceSerializer(obj.sector, many=True)
            if get_data.data:
                context = get_data.data[0]
        return context

    def get_tender_type(self, obj):
        context = {}
        if obj.sector:
            get_data = OpportunityTypeSerializer(obj.tender_type, many=True)
            if get_data.data:
                context = get_data.data[0]
        return context

    def get_is_editable(self, obj):
        is_editable_record = False
        if 'user' in self.context:
            user = self.context['user']
            is_editable_record = AppliedTender.objects.filter(
                tender=obj,
                user=user,
                shortlisted_at = None,
                rejected_at = None,
                created__date__gte = date.today()
            ).exists()
        return is_editable_record

    def get_application(self, obj):
        application_context = dict()
        if 'user' in self.context:
            user = self.context['user']
            if AppliedTender.objects.filter(tender=obj, user=user).exists():
                application = AppliedTender.objects.get(tender=obj, user=user)
                application_context['id'] = application.id
                application_context['created'] = application.created
        return application_context


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
            'sector', 'deadline', 'budget_min', 'budget_max', 'tender_category', 'tag',
            'is_notification'
        ]

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        return instance


class GetTenderFilterSerializers(serializers.ModelSerializer):
    """
    `GetTenderFilterSerializers` is a class-based serializer that inherits from the `ModelSerializer` class of the
    Django REST Framework.
    It defines a Meta class that specifies the TenderFilter model and the fields to be included in the serialization,
    as well as additional SerializerMethodFields.

    Attributes:
        - `model (class)`: The Django model class that this serializer is based on.
        - `fields (list)`: A list of fields to be included in the serialized output, including additional fields
            generated by `SerializerMethodFields`.

    Usage:
        - This serializer can be used to serialize TenderFilter objects and convert them to JSON format for use in HTTP
            responses.
        - In addition to the standard fields specified in the Meta class, this serializer also includes
            `SerializerMethodFields` for 'country', 'city'.
        - These fields are generated by calling the corresponding methods on the serializer instance and returning
            their values.
        - The resulting serialized output will include the standard fields as well as the additional fields generated
            by the SerializerMethodFields.
    """

    country = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    tender_category = serializers.SerializerMethodField()
    tag = serializers.SerializerMethodField()
    opportunity_type = serializers.SerializerMethodField()
    sector = serializers.SerializerMethodField()

    class Meta:
        model = TenderFilter
        fields = [
            'id', 'title', 'country', 'city', 'opportunity_type',
            'sector', 'deadline', 'budget_min', 'budget_max', 'tender_category', 'tag',
            'is_notification'
        ]

    def get_country(self, obj):
        """Get the serialized country data for a TenderFilter object.

        This method uses the CountrySerializer to serialize the country associated with a TenderFilter
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A TenderFilter object whose country data will be serialized.

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
        """Get the serialized city data for a TenderFilter object.

        This method uses the CitySerializer to serialize the city associated with a TenderFilter
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A TenderFilter object whose city data will be serialized.

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

    def get_opportunity_type(self, obj):
        """
        Get the serialized opportunity type data for a TenderDetails object.

        This method uses the ChoiceSerializer to serialize the tender categories associated with a TenderDetails
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A TenderDetails object whose opportunity type data will be serialized.

        Returns:
            A dictionary containing the serialized opportunity type data, or an empty dictionary if the
            serializer did not return any data.

        """

        context = []
        get_data = OpportunityTypeSerializer(obj.opportunity_type, many=True)
        if get_data.data:
            context = get_data.data
        return context
    
    def get_sector(self, obj):
        """
        Get the serialized sector data for a TenderDetails object.

        This method uses the ChoiceSerializer to serialize the tender categories associated with a TenderDetails
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A TenderDetails object whose sector data will be serialized.

        Returns:
            A dictionary containing the serialized sector data, or an empty dictionary if the
            serializer did not return any data.

        """

        context = []
        get_data = ChoiceSerializer(obj.sector, many=True)
        if get_data.data:
            context = get_data.data
        return context


class TendersSuggestionSerializers(serializers.ModelSerializer):
    """
    Serializer for the `TenderDetails` model.
            
    """
    country = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    
    class Meta:
        model = TenderDetails
        fields = [
            'id', 'title', 'budget_amount', 'budget_currency', 'country', 'city',
            'created', 'address', 'slug'
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


class AppliedTenderSerializers(serializers.ModelSerializer):
    """
    Serializer for the AppliedTender model.
    """

    user = serializers.SerializerMethodField()
    tender = serializers.SerializerMethodField()

    class Meta:
        model = AppliedTender
        fields = [
            'id', 'shortlisted_at', 'rejected_at', 'created', 
            'short_letter', 'user', 'tender'
        ]

    def get_user(self, obj):
        """
        Returns the serialized representation of the user related to the applied tender.

        Parameters:
            - obj: AppliedTender instance

        Returns:
            - Serialized representation of the user related to the applied tender.
        """

        context = {}
        get_data = UserSerializer(obj.user)
        if get_data.data:
            context = get_data.data
        return context

    def get_tender(self, obj):
        """
        Returns a dictionary with the ID and title of the tender related to the applied tender.

        Parameters:
            - obj: AppliedTender instance

        Returns:
            - Dictionary with the ID and title of the tender related to the applied tender.
        """
        
        return {"id": obj.tender.id, "title": obj.tender.title}
