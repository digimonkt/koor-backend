# IMPORT PYTHON PACKAGE.
from rest_framework import exceptions, status
from rest_framework import serializers

from project_meta.models import Media
from user_profile.models import EmployerProfile


class UpdateEmployerAboutSerializers(serializers.ModelSerializer):
    """
    Created a serializer class for update employer about. Here we use ModelSerializer, using EmployerProfile model.
    After update employer profile data we return employer profile instance.
    """
    display_name = serializers.CharField(style={"input_type": "text"}, write_only=True, allow_blank=False)
    license_file = serializers.FileField(style={"input_type": "file"}, write_only=True, allow_null=False)

    class Meta:
        model = EmployerProfile
        fields = ['organization_type', 'market_information_notification', 'other_notification', 'license_id',
                  'display_name', 'license_file']

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        if 'display_name' in validated_data:
            instance.user.display_name = validated_data['display_name']
            instance.user.save()
        if 'license_file' in validated_data:
            # Get media type from upload license file
            content_type = str(validated_data['license_file'].content_type).split("/")
            if content_type[0] == "application":
                media_type = 'document'
            else:
                media_type = content_type[0]
            # save media file into media table and get instance of saved data.
            media_instance = Media(file_path=validated_data['license_file'], media_type=media_type)
            media_instance.save()
            # save media instance into license id file into employer profile table.
            instance.license_id_file = media_instance
            instance.save()
        return instance
