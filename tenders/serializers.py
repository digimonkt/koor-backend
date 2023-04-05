from rest_framework import serializers

from tenders.models import TenderDetails, TenderCategory

from users.serializers import UserSerializer


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
