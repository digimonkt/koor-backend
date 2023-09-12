from rest_framework import serializers

from job_seekers.serializers import GetAppliedJobsNotificationSerializers
from notification.models import Notification


class GetNotificationSerializers(serializers.ModelSerializer):

    """
    A serializer class for Notification objects, with a custom field for the application data.

    The `application` field is a SerializerMethodField that returns the data of the related Application object,
    serialized using the `GetAppliedJobsNotificationSerializers` class.

    Attributes:
        application: A SerializerMethodField that returns the data of the related Application object.

    Meta:
        model: The Notification model class to be serialized.
        fields: A list of field names to be included in the serialized representation.

    Methods:
        get_application(obj): Returns the serialized data of the related Application object.

    """

    application = serializers.SerializerMethodField()
    job = serializers.SerializerMethodField()
    job_filter = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'notification_type', 'message', 'application','job', 
            'job_filter', 'seen', 'created', 'message_sender', 'conversation_id'
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
        if obj.application:
            get_data = GetAppliedJobsNotificationSerializers(obj.application)
            if get_data.data:
                return get_data.data
        return None
    
    def get_job(self, obj):
        if obj.job:
            user = dict()
            user['id'] = obj.job.user.id
            user['name'] = obj.job.user.name
            user['email'] = obj.job.user.email
            if obj.job.user.image:
                if obj.job.user.image.title == "profile image":
                    user['image'] = str(obj.job.user.image.file_path)
                else:
                    user['image'] = obj.job.user.image.file_path.url
            return {"id": obj.job.id, "title": obj.job.title, 'user': user}
        return None
    
    def get_job_filter(self, obj):
        if obj.job_filter:
            return {"id": obj.job_filter.id, "title": obj.job_filter.title}
        return None
