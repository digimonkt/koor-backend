from rest_framework import serializers

from job_seekers.serializers import GetAppliedJobsSerializers
from notification.models import Notification


class GetNotificationSerializers(serializers.ModelSerializer):

    """
    A serializer class for Notification objects, with a custom field for the application data.

    The `application` field is a SerializerMethodField that returns the data of the related Application object,
    serialized using the `GetAppliedJobsSerializers` class.

    Attributes:
        application: A SerializerMethodField that returns the data of the related Application object.

    Meta:
        model: The Notification model class to be serialized.
        fields: A list of field names to be included in the serialized representation.

    Methods:
        get_application(obj): Returns the serialized data of the related Application object.

    """

    application = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'notification_type', 'application', 'job_filter', 'seen', 'created'
        ]

    def get_application(self, obj):
        """
        Returns the serialized data of the related Application object.

        Args:
            obj: The Notification object being serialized.

        Returns:
            A dictionary containing the serialized data of the related Application object,
            or an empty dictionary if the related object does not exist or could not be serialized.

        """
        return_context = {}
        get_data = GetAppliedJobsSerializers(obj.application, context={"request": self.context['request']})
        if get_data.data:
            return_context = get_data.data
        return return_context
