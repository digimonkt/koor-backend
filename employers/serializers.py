from rest_framework import serializers

from jobs.models import JobDetails
from project_meta.models import Media, Skill, Language

from user_profile.models import EmployerProfile
from users.models import User

from jobs.models import JobCategory, JobAttachmentsItem


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
        fields = ['organization_name', 'mobile_number', 'country_code', 'organization_type',
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
                    if len(mobile_number) > 13:
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
            if content_type[0] not in ["video", "image" ] :
                media_type = 'document'
            else:
                media_type = content_type[0]
            # save media file into media table and get instance of saved data.
            media_instance = Media(title=validated_data['license'].name, file_path=validated_data['license'], media_type=media_type)
            media_instance.save()
            # save media instance into license id file into employer profile table.
            instance.license_id_file = media_instance
            instance.save()
        return instance


class CreateJobsSerializers(serializers.ModelSerializer):
    """
    Serializer class for creating job details.

    This serializer class is based on the `serializers.ModelSerializer` class and extends its functionality to handle
    the creation of job details objects. The serializer handles the following fields:
        - `title`: title of the job
        - `budget_currency`: currency of the budget amount
        - `budget_amount`: amount of the budget
        - `budget_pay_period`: period of payment for the budget
        - `description`: description of the job
        - `country`: country where the job is located
        - `city`: city where the job is located
        - `address`: address of the job location
        - `job_category`: categories related to the job
        - `is_full_time`: boolean indicating if the job is full-time
        - `is_part_time`: boolean indicating if the job is part-time
        - `has_contract`: boolean indicating if the job has a contract
        - `contact_email`: contact email for the job
        - `contact_phone`: contact phone for the job
        - `contact_whatsapp`: contact WhatsApp for the job
        - `highest_education`: highest education required for the job
        - `language`: languages required for the job
        - `skill`: skills required for the job

    The `job_category`, `language`, and `skill` fields are related fields that are read-only.
    """
    job_category = serializers.PrimaryKeyRelatedField(
        queryset=JobCategory.objects.all(),
        many=True,
        write_only=True
    )
    language = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all(),
        many=True,
        write_only=True
    )
    skill = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
        many=True,
        write_only=True
    )
    attachments = serializers.ListField(
        style={"input_type": "file"},
        write_only=True,
        allow_null=False,
        required=False
    )

    class Meta:
        model = JobDetails
        fields = [
            'title', 'budget_currency', 'budget_amount', 'budget_pay_period', 'description', 'country',
            'city', 'address', 'job_category', 'is_full_time', 'is_part_time', 'has_contract',
            'contact_email', 'contact_phone', 'contact_whatsapp', 'highest_education', 'language', 'skill',
            'working_days', 'attachments','deadline'
        ]

    def validate_job_category(self, job_category):
        """
        validate_job_category - A function to validate the job category for a job instance.

        Parameters:
            job_category (str): The job category to be validated.

        Returns:
            job_category (str): The validated job category.

            This function validates the job category of a job instance. If the job category is an empty string, a
        ValidationError is raised with a message indicating that the job category cannot be blank. If the length of
        the job category string is greater than 3, a ValidationError is raised with a message indicating that the
        choices are limited to 3. If the job category is not blank and its length is within limits, the job category
        is returned.
        """
        if job_category == '':
            limit = 3
            if len(job_category) > limit:
                raise serializers.ValidationError({'job_category': 'Choices limited to ' + str(limit)})
            raise serializers.ValidationError({'job_category': 'Job category can not be blank.'})
        else:
            return job_category

    def validate_language(self, language):
        """
        validate_language - A function to validate the language for a job instance.

        Parameters:
            language (str): The language to be validated.

        Returns:
            language (str): The validated language.

        This function validates the language of a job instance. If the language is an empty string, a ValidationError
        is raised with a message indicating that the language cannot be blank. If the length of the language string is
        greater than 3, a ValidationError is raised with a message indicating that the choices are limited to 3. If
        the language is not blank and its length is within limits, the language is returned.
        """
        if language == '':
            limit = 3
            if len(language) > limit:
                raise serializers.ValidationError({'language': 'Choices limited to ' + str(limit)})
            raise serializers.ValidationError({'language': 'Language can not be blank.'})
        else:
            return language

    def validate_skill(self, skill):
        """
        validate_skill - A function to validate the skill for a job instance.

        Parameters:
            skill (str): The skill to be validated.

        Returns:
            skill (str): The validated skill.

        This function validates the skill of a job instance. If the skill is an empty string, a ValidationError is
        raised with a message indicating that the skill cannot be blank. If the length of the skill string is greater
        than 3, a ValidationError is raised with a message indicating that the choices are limited to 3. If the skill
        is not blank and its length is within limits, the skill is returned.
        """
        if skill == '':
            limit = 3
            if len(skill) > limit:
                raise serializers.ValidationError({'skill': 'Choices limited to ' + str(limit)})
            raise serializers.ValidationError({'skill': 'Skill can not be blank.'})
        else:
            return skill

    def save(self, user):
        """
            save - A function to save the validated data and its attachments (if any) for a job instance.
        
        Parameters:
            - user (object): The user for whom the job instance is being saved.
        
        Returns:
            - self (object): The instance of the class.
        
        This function saves the validated data of a job instance, and if there are any attachments in the validated
        data, it saves them as well. The attachments are saved in the 'Media' table and the relation between the job
        instance and the attachments is saved in the 'JobAttachmentsItem' table. The media type of the attachment is
        determined based on its content type, with application types being saved as 'documents' and other types being
        saved as their content type.
        """
        attachments = None
        if 'attachments' in self.validated_data:
            attachments = self.validated_data.pop('attachments')
        job_instance = super().save(user=user, status='active')
        if attachments:
            for attachment in attachments:
                content_type = str(attachment.content_type).split("/")
                if content_type[0] not in ["video", "image" ] :
                    media_type = 'document'
                else:
                    media_type = content_type[0]
                # save media file into media table and get instance of saved data.
                media_instance = Media(title=attachment.name, file_path=attachment, media_type=media_type)
                media_instance.save()
                # save media instance into license id file into employer profile table.
                attachments_instance = JobAttachmentsItem.objects.create(job=job_instance, attachment=media_instance)
                attachments_instance.save()
        return self


class UserSerializer(serializers.ModelSerializer):
    """
    A serializer class for User model that includes `'id'`, `'name'`, `'email'`, `'country_code'`, `'mobile_number'`,
    and `'image'` fields.
    The 'image' field is a `SerializerMethodField` that returns the URL of the user's image if it exists, otherwise None.

    Attributes:
        - `image (serializers.SerializerMethodField)`: a SerializerMethodField that returns the URL of the user's image
        if it exists, otherwise None.

    Methods:
        - `get_image(obj)`: A method that takes a User instance and returns the URL of the user's image if it exists,
        otherwise None.

    """
    image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'email',
            'country_code',
            'mobile_number',
            'image',
        )

    def get_image(self, obj):
        context = {}
        if obj.image:
            context['title'] = obj.image.title
            context['path'] = obj.image.file_path.url
            context['type'] = obj.image.media_type
            return context
        return None

