import json

from rest_framework import serializers

from jobs.models import JobDetails

from project_meta.models import (
    Media, Skill, Language,
    Tag
)

from tenders.models import (
    TenderDetails,
    TenderCategory,
    TenderAttachmentsItem
)

from user_profile.models import EmployerProfile
from users.models import User

from jobs.models import (
    JobCategory,
    JobAttachmentsItem,
    JobsLanguageProficiency
)


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
            raise serializers.ValidationError('License id can not be blank.', code='license_id')
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
        if mobile_number and country_code in ["", None]:
            raise serializers.ValidationError({'country_code': 'Country code can not be blank.'})
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
            if content_type[0] not in ["video", "image"]:
                media_type = 'document'
            else:
                media_type = content_type[0]
            # save media file into media table and get instance of saved data.
            media_instance = Media(title=validated_data['license'].name, file_path=validated_data['license'],
                                   media_type=media_type)
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
    skill = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
        many=True,
        write_only=True,
        allow_null=True,
        required=False
    )
    language = serializers.ListField(
        style={"input_type": "text"},
        write_only=True,
        allow_null=True,
        required=False
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
            'duration','experience', 'attachments', 'deadline', 'start_date'
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
        if job_category not in [None, ""]:
            limit = 3
            if len(job_category) > limit:
                raise serializers.ValidationError({'job_category': 'Choices limited to ' + str(limit)})
            return job_category
        else:
            raise serializers.ValidationError({'job_category': 'Job category can not be blank.'})

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
        if language not in [""]:
            limit = 3
            if len(language) > limit:
                raise serializers.ValidationError({'language': 'Choices limited to ' + str(limit)})
            for language_data in language:
                language_data = json.loads(language_data)
                if 'language' not in language_data:
                    raise serializers.ValidationError('This field is required.', code='language')
                else:
                    try:
                        if Language.objects.get(id=language_data['language']):
                            pass
                    except Language.DoesNotExist:
                        raise serializers.ValidationError('Language not exist.', code='language')
                if 'written' not in language_data:
                    raise serializers.ValidationError({'language_written': 'Language written proficiency is required.'})
                if 'spoken' not in language_data:
                    raise serializers.ValidationError({'language_spoken': 'Language spoken proficiency is required.'})
            return language
        else:
            raise serializers.ValidationError('This field is required.', code='language')

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
        if skill not in [""]:
            limit = 3
            if len(skill) > limit:
                raise serializers.ValidationError({'skill': 'Choices limited to ' + str(limit)})
            return skill
        else:
            raise serializers.ValidationError({'skill': 'Skill can not be blank.'})

    def validate(self, data):
        job_category = data.get("job_category")
        if not job_category:
            raise serializers.ValidationError({'job_category': 'This field is required.'})
        return data

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
        language = None
        attachments = None

        if 'language' in self.validated_data:
            language = self.validated_data.pop('language')
        if 'attachments' in self.validated_data:
            attachments = self.validated_data.pop('attachments')
        job_instance = super().save(user=user, status='active')
        if language:
            for language_data in language:
                language_data = json.loads(language_data)
                language_instance = Language.objects.get(id=language_data['language'])
                job_language_instance = JobsLanguageProficiency.objects.create(
                    job=job_instance,
                    language=language_instance,
                    spoken=language_data['spoken'],
                    written=language_data['written']
                )
                job_language_instance.save()
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
                attachments_instance = JobAttachmentsItem.objects.create(job=job_instance, attachment=media_instance)
                attachments_instance.save()
        return self


class UpdateJobSerializers(serializers.ModelSerializer):
    """
    Serializer class for updating JobDetails model instances.
    This class defines a set of fields to be updated and provides validation methods for job_category, language and
    skill fields. Additionally, it handles the updating of the attachments and attachments_remove fields. It takes an
    existing instance of JobDetails and validated data, then performs the update operation on the instance.
    Attributes:
        - `job_category`: PrimaryKeyRelatedField to JobCategory model objects, many to many relationship, used to update
        job categories.
        - `language`: PrimaryKeyRelatedField to Language model objects, many to many relationship, used to update
        languages.
        - `skill`: PrimaryKeyRelatedField to Skill model objects, many to many relationship, used to update skills.
        - `attachments`: ListField of file inputs, used to add new attachments to the job instance.
        - `attachments_remove`: ListField of text inputs, used to remove attachments from the job instance.
    Methods:
        - `validate_job_category`: validates the job_category field and raises a ValidationError if the value is empty
        or exceeds a specified limit.
        - `validate_language`: validates the language field and raises a ValidationError if the value is empty or
        exceeds a specified limit.
        - `validate_skill`: validates the skill field and raises a ValidationError if the value is empty or exceeds a
        specified limit.
        - `update`: performs the update operation on the JobDetails instance and handles the updating of the attachments
         and attachments_remove fields.
    """

    job_category = serializers.PrimaryKeyRelatedField(
        queryset=JobCategory.objects.all(),
        many=True,
        write_only=True
    )
    skill = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
        many=True,
        write_only=True,
        required=False
    )
    language = serializers.ListField(
        style={"input_type": "text"},
        write_only=True,
        required=False
    )
    language_remove = serializers.ListField(
        style={"input_type": "text"},
        write_only=True,
        allow_null=False
    )
    attachments = serializers.ListField(
        style={"input_type": "file"},
        write_only=True,
        allow_null=False,
        required=False
    )
    attachments_remove = serializers.ListField(
        style={"input_type": "text"},
        write_only=True,
        allow_null=False
    )

    class Meta:
        model = JobDetails
        fields = [
            'title', 'budget_currency', 'budget_amount', 'budget_pay_period', 'description', 'country',
            'city', 'address', 'job_category', 'is_full_time', 'is_part_time', 'has_contract',
            'contact_email', 'contact_phone', 'contact_whatsapp', 'highest_education', 'language', 'language_remove',
            'skill', 'duration', 'experience', 'status', 'attachments', 'attachments_remove', 'deadline', 'start_date'
        ]

    def validate_job_category(self, job_category):
        if job_category not in [None, ""]:
            limit = 3
            if len(job_category) > limit:
                raise serializers.ValidationError({'job_category': 'Choices limited to ' + str(limit)})
            return job_category
        else:
            raise serializers.ValidationError({'job_category': 'Job category can not be blank.'})

    def validate_language(self, language):
        if language not in [""]:
            limit = 3
            if len(language) > limit:
                raise serializers.ValidationError({'language': 'Choices limited to ' + str(limit)})
            for language_data in language:
                language_data = json.loads(language_data)
                if 'language' not in language_data:
                    raise serializers.ValidationError('This field is required.', code='language')
                else:
                    try:
                        if Language.objects.get(id=language_data['language']):
                            pass
                    except Language.DoesNotExist:
                        raise serializers.ValidationError('Language not exist.', code='language')
                if 'written' not in language_data:
                    raise serializers.ValidationError({'language_written': 'Language written proficiency is required.'})
                if 'spoken' not in language_data:
                    raise serializers.ValidationError({'language_spoken': 'Language spoken proficiency is required.'})
            return language
        else:
            raise serializers.ValidationError({'language': 'Language can not be blank.'})

    def validate_skill(self, skill):
        if skill not in [""]:
            limit = 3
            if len(skill) > limit:
                raise serializers.ValidationError({'skill': 'Choices limited to ' + str(limit)})
            return skill
        else:
            raise serializers.ValidationError({'skill': 'Skill can not be blank.'})

    def validate(self, data):
        job_category = data.get("job_category")
        if not job_category:
            raise serializers.ValidationError({'job_category': 'This field is required.'})
        return data

    def update(self, instance, validated_data):
        """
            Update an existing Job instance and related fields with new validated data.

            `Args`:
                - `instance`: A Job instance to be updated.
                - `validated_data`: A dictionary of validated data for the Job instance.

            `Returns`:
                - The updated Job instance.

            - The function first extracts validated data for 'language', 'language_remove', 'attachments', and
            'attachments_remove' from the given `validated_data` dictionary, if they exist.

            - It then calls the `update` method of the superclass with the given `instance` and `validated_data`.

            - If `attachments_remove` exists, it iterates over the `attachments_remove` list and removes the
            corresponding `JobAttachmentsItem` instances from the database.

            - If `language_remove` exists, it iterates over the `language_remove` list and removes the corresponding
            `JobsLanguageProficiency` instances from the database.

            - If `language` exists, it iterates over the `language` list and creates or updates
            `JobsLanguageProficiency` instances for the given `instance`.

            - If `attachments` exists, it iterates over the `attachments` list and creates new `Media` and
            `JobAttachmentsItem` instances for the given `instance`.

            - Finally, it returns the updated `instance`.
        """
        attachments = None
        attachments_remove = None
        language = None
        language_remove = None

        if 'language' in self.validated_data:
            language = self.validated_data.pop('language')
        if 'language_remove' in self.validated_data:
            language_remove = self.validated_data.pop('language_remove')
        if 'attachments' in self.validated_data:
            attachments = self.validated_data.pop('attachments')
        if 'attachments_remove' in self.validated_data:
            attachments_remove = self.validated_data.pop('attachments_remove')

        super().update(instance, validated_data)
        if attachments_remove:
            for remove in attachments_remove:
                JobAttachmentsItem.objects.filter(id=remove).update(job=None)
        if language_remove:
            for remove in language_remove:
                JobsLanguageProficiency.objects.filter(id=remove).delete()
        if language:
            for language_data in language:
                language_data = json.loads(language_data)
                language_instance = Language.objects.get(id=language_data['language'])
                if not JobsLanguageProficiency.objects.filter(job=instance, language=language_instance).exists():
                    if 'id' in language_data:
                        job_language_instance = JobsLanguageProficiency.objects.get(id=language_data['id'])
                        job_language_instance.job = instance
                        job_language_instance.language = language_instance
                        job_language_instance.spoken = language_data['spoken']
                        job_language_instance.written = language_data['written']
                        job_language_instance.save()
                    else:
                        job_language_instance = JobsLanguageProficiency.objects.create(
                            job=instance,
                            language=language_instance,
                            spoken=language_data['spoken'],
                            written=language_data['written']
                        )
                        job_language_instance.save()
        if attachments:
            for attachment in attachments:
                content_type = str(attachment.content_type).split("/")
                if content_type[0] not in ["video", "image"]:
                    media_type = 'document'
                else:
                    media_type = content_type[0]
                media_instance = Media(title=attachment.name, file_path=attachment, media_type=media_type)
                media_instance.save()
                attachments_instance = JobAttachmentsItem.objects.create(job=instance, attachment=media_instance)
                attachments_instance.save()
        return instance


class CreateTendersSerializers(serializers.ModelSerializer):
    """
    Serializer for creating `TenderDetails` instances.

    Fields:
        - `title (str)`: The title of the tender.
        - `budget_currency (str)`: The currency used for the tender budget.
        - `budget_amount (float)`: The amount of the tender budget.
        - `description (str)`: A description of the tender.
        - `country (str)`: The country where the tender is located.
        - `city (str)`: The city where the tender is located.
        - `tender_category (PrimaryKeyRelatedField)`: The category/categories of the tender. Accepts a list of primary
            keys.
        - `tender_type (str)`: The type of the tender.
        - `sector (str)`: The sector of the tender.
        - `tag (PrimaryKeyRelatedField)`: The tag/tags of the tender. Accepts a list of primary keys.

    Methods:
        - `validate_tender_category(self, tender_category)`: Validates the tender category field. Raises a
            `ValidationError` if there are more than `3 categories`.
        - `validate_tag(self, tag)`: Validates the tag field. Raises a `ValidationError` if there are more than
            `3 tags`.
        - `validate(self, data)`: Validates the `tender_category` and `tag` fields. Raises a ValidationError if they
            are missing.
        - `save(self, user)`: Saves the TenderDetails instance and creates `TenderAttachmentsItem` instances for any
            attachments.

    """

    tender_category = serializers.PrimaryKeyRelatedField(
        queryset=TenderCategory.objects.all(),
        many=True,
        write_only=True
    )
    tag = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
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
        model = TenderDetails
        fields = [
            'title', 'budget_currency', 'budget_amount', 'description', 'country', 'city',
            'tender_category', 'tender_type', 'sector', 'tag', 'attachments', 'deadline', 
            'start_date'
        ]

    def validate_tender_category(self, tender_category):
        if tender_category not in [None, ""]:
            limit = 3
            if len(tender_category) > limit:
                raise serializers.ValidationError({'tender_category': 'Choices limited to ' + str(limit)})
            return tender_category
        else:
            raise serializers.ValidationError({'tender_category': 'Tender category can not be blank.'})

    def validate_tag(self, tag):
        if tag not in [None, ""]:
            limit = 3
            if len(tag) > limit:
                raise serializers.ValidationError({'tag': 'Choices limited to ' + str(limit)})
            return tag
        else:
            raise serializers.ValidationError({'tag': 'Tag can not be blank.'})

    def save(self, user):
        attachments = None
        if 'attachments' in self.validated_data:
            attachments = self.validated_data.pop('attachments')
        tender_instance = super().save(user=user, status='active')

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
                attachments_instance = TenderAttachmentsItem.objects.create(tender=tender_instance,
                                                                            attachment=media_instance)
                attachments_instance.save()
        return self


class UpdateTenderSerializers(serializers.ModelSerializer):
    """
    A serializer that handles the validation and updating of tender details for a PUT request.

    Args:
        - `serializers.ModelSerializer`: Inherits from the Django REST Framework's ModelSerializer.

    Behaviour:
        - Defines various fields as PrimaryKeyRelatedField and ListField for the tender category, tags, and attachments
            of a tender. Validates these fields with custom validation methods.
        - Defines a Meta class to specify the model and fields to be used in the serializer.
        - Validates the tender category and tags fields and raises validation errors if necessary. Also ensures that
            these fields are not empty.
        - Overrides the update() method to allow updating of tender details, attachments, and attachment removal.

    """

    tender_category = serializers.PrimaryKeyRelatedField(
        queryset=TenderCategory.objects.all(),
        many=True,
        write_only=True
    )
    tag = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        write_only=True
    )
    attachments = serializers.ListField(
        style={"input_type": "file"},
        write_only=True,
        allow_null=False,
        required=False
    )
    attachments_remove = serializers.ListField(
        style={"input_type": "text"},
        write_only=True,
        allow_null=False
    )

    class Meta:
        model = TenderDetails
        fields = [
            'title', 'budget_currency', 'budget_amount', 'description', 'country', 'city',
            'tender_category', 'tender_type', 'sector', 'tag', 'attachments', 'attachments_remove'
        ]

    def validate_tender_category(self, tender_category):
        if tender_category not in [None, ""]:
            limit = 3
            if len(tender_category) > limit:
                raise serializers.ValidationError({'tender_category': 'Choices limited to ' + str(limit)})
            return tender_category
        else:
            raise serializers.ValidationError({'tender_category': 'Tender category can not be blank.'})

    def validate_tag(self, tag):
        if tag not in [None, ""]:
            limit = 3
            if len(tag) > limit:
                raise serializers.ValidationError({'tag': 'Choices limited to ' + str(limit)})
            return tag
        else:
            raise serializers.ValidationError({'tag': 'Tag can not be blank.'})

    def validate(self, data):
        tender_category = data.get("tender_category")
        tag = data.get("tag")
        if not tender_category:
            raise serializers.ValidationError({'tender_category': 'This field is required.'})
        if not tag:
            raise serializers.ValidationError({'tag': 'This field is required.'})
        return data

    def update(self, instance, validated_data):
        attachments = None
        attachments_remove = None

        if 'attachments' in self.validated_data:
            attachments = self.validated_data.pop('attachments')
        if 'attachments_remove' in self.validated_data:
            attachments_remove = self.validated_data.pop('attachments_remove')

        super().update(instance, validated_data)
        if attachments_remove:
            for remove in attachments_remove:
                TenderAttachmentsItem.objects.filter(id=remove).update(tender=None)

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
                attachments_instance = TenderAttachmentsItem.objects.create(tender=tender_instance,
                                                                            attachment=media_instance)
                attachments_instance.save()
        return instance
