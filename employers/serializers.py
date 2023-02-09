from rest_framework import serializers

from project_meta.models import Media
from user_profile.models import EmployerProfile
from users.models import User


class UpdateAboutSerializers(serializers.ModelSerializer):
    """
    UpdateAboutSerializers:
        A Django REST framework serializer for updating information of an EmployerProfile model instance.

    Fields:
        - organization_name: A CharField that represents the name of the organization. It has an input type of "text"
                             and is write-only. It cannot be blank.
        - mobile_number: A CharField that represents the mobile number of the organization. It has an input type of
                         "text" and is write-only. It cannot be blank and must contain only numbers.
        - country_code: A CharField that represents the country code for the mobile number. It has an input type of
                        "text" and is write-only. It cannot be blank.
        - license: A FileField that represents the license of the organization. It has an input type of "file" and is
                   write-only. It cannot be null.

    Methods:
        - validate_license_id: Validates the license_id field and raises a ValidationError if it is blank.
        - validate_mobile_number: Validates the mobile_number field and raises a ValidationError if it is not a digit,
          too long, already in use, or blank.
        - validate: Validates the country_code, mobile_number, license_id, and license fields.
        
    Raises a ValidationError if any of the fields are blank when the corresponding field is present.
        - update: Updates the EmployerProfile instance with the validated data. It updates the User model with the
                  organization_name and mobile_number fields. The license field is saved in the Media model and the
                  instance is linked to the license_id_file field in the EmployerProfile model.

    Note:
        The EmployerProfile model must have the fields specified in the 'fields' attribute of the Meta class.
        The User model must have the fields 'name', 'mobile_number', and 'country_code'.
    """
    organization_name = serializers.CharField(
        style={"input_type": "text"},
        write_only=True,
        allow_blank=False
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
    license = serializers.FileField(
        style={"input_type": "file"},
        write_only=True,
        allow_null=False
    )

    class Meta:
        model = EmployerProfile
        fields = ['organization_name', 'mobile_number',  'country_code', 'organization_type',
                  'market_information_notification', 'other_notification', 'license_id', 'license']
        
    def validate_license_id(self, license_id):
        if license_id == '':
            raise serializers.ValidationError('License id can not be blank sfs', code='license_id')
        else:
            return license_id
    
    def validate_mobile_number(self, mobile_number):
        if mobile_number != '':
            if mobile_number.isdigit():
                try:
                    if len(mobile_number) > 13 :
                        raise serializers.ValidationError('This is an invalid mobile number.', code='mobile_number')
                    else:
                        if User.objects.get(mobile_number=mobile_number):
                            raise serializers.ValidationError('Mobile number already in use.', code='mobile_number')
                except User.DoesNotExist:
                    return mobile_number
            else:
                raise serializers.ValidationError('Mobile number must contain only numbers', code='mobile_number')
        else:
            raise serializers.ValidationError('Mobile number can not be blank', code='mobile_number')
        
    def validate(self, data):
        country_code = data.get("country_code")
        mobile_number = data.get("mobile_number")
        license_id = data.get("license_id")
        license = data.get("license")
        if mobile_number and country_code in ["", None]:
            raise serializers.ValidationError({'country_code': 'Country code can not be blank.'})
        if license_id and license in ["", None]:
            raise serializers.ValidationError({'license': 'License can not be blank.'})
        if license and license_id in ["", None]:
            raise serializers.ValidationError({'license_id': 'License id can not be blank. hkhkh'})
        return data

    def update(self, instance, validated_data):
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
            if content_type[0] == "application":
                media_type = 'document'
            else:
                media_type = content_type[0]
            # save media file into media table and get instance of saved data.
            media_instance = Media(file_path=validated_data['license'], media_type=media_type)
            media_instance.save()
            # save media instance into license id file into employer profile table.
            instance.license_id_file = media_instance
            instance.save()
        return instance
