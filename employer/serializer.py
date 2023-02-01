# IMPORT PYTHON PACKAGE.
from rest_framework import serializers

from project_meta.models import Media
from user_profile.models import EmployerProfile


class UpdateEmployerAboutSerializers(serializers.ModelSerializer):
    """
    Created a serializer class for update employer profile data. Here we use ModelSerializer.
    Here we use update function of modelSerializer for update data and we set default model validation.
    """
    display_name = serializers.CharField(
        style={"input_type": "text"},
        write_only=True,
        required=False,
        allow_blank=False
    )
    license_id = serializers.CharField(
        style={"input_type": "text"},
        write_only=True,
        required=False,
        allow_blank=False
    )
    license_file = serializers.FileField(
        style={"input_type": "file"},
        write_only=True,
        required=False
    )

    class Meta:
        model = EmployerProfile
        fields = ['organization_type', 'market_information_notification', 'other_notification', 'license_id',
                  'display_name', 'license_file']

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        if validated_data.get('display_name'):
            instance.user.display_name = validated_data.get('display_name')
            instance.user.save()

        if validated_data.get('license_file'):
            content_type = str(validated_data.get('license_file').content_type)
            content_type = content_type.split("/")[0]
            if content_type == "application":
                content_type = 'document'

            media_instance = Media(file_path=validated_data.get('license_file'), media_type=content_type).save()
            instance.license_id_file = media_instance

        instance.save()
        return instance
