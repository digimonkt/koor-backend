from datetime import date
from django.db.models import Sum
import json

from rest_framework import serializers

from job_seekers.models import AppliedJob

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
from users.serializers import UserSerializer

from jobs.models import (
    JobCategory,
    JobAttachmentsItem,
    JobsLanguageProficiency,
    JobDetails,
    JobSubCategory,
    JobShare
)

from .models import BlackList


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
                  'market_information_notification', 'other_notification', 'license_id', 'license',
                  'description', 'address', 'website', 'country',  'city']

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
        - `job_sub_category`: sub-categories related to the job
        - `is_full_time`: boolean indicating if the job is full-time
        - `is_part_time`: boolean indicating if the job is part-time
        - `has_contract`: boolean indicating if the job has a contract
        - `contact_email`: contact email for the job
        - `cc1`: cc1 for the job
        - `cc2`: cc2 for the job
        - `contact_whatsapp`: contact WhatsApp for the job
        - `highest_education`: highest education required for the job
        - `language`: languages required for the job
        - `skill`: skills required for the job

    The `job_category`, `job_sub_category`, `language`, and `skill` fields are related fields that are read-only.
    """
    job_category = serializers.PrimaryKeyRelatedField(
        queryset=JobCategory.objects.all(),
        many=True,
        write_only=True
    )
    job_sub_category = serializers.PrimaryKeyRelatedField(
        queryset=JobSubCategory.objects.all(),
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
            'city', 'address', 'job_category', 'job_sub_category', 'is_full_time', 'is_part_time', 'has_contract',
            'contact_email', 'cc1', 'cc2', 'contact_whatsapp', 'highest_education', 'language', 'skill',
            'duration', 'experience', 'attachments', 'deadline', 'start_date'
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

    def validate_job_sub_category(self, job_sub_category):
        """
        validate_job_sub_category - A function to validate the job sub category for a job instance.

        Parameters:
            job_sub_category (str): The job category to be validated.

        Returns:
            job_sub_category (str): The validated job sub category.

            This function validates the job category of a job instance. If the job sub category is an empty string, a
        ValidationError is raised with a message indicating that the job sub category cannot be blank. If the length of
        the job sub category string is greater than 3, a ValidationError is raised with a message indicating that the
        choices are limited to 3. If the job sub category is not blank and its length is within limits, the job sub category
        is returned.
        """
        if job_sub_category not in [None, ""]:
            limit = 3
            if len(job_sub_category) > limit:
                raise serializers.ValidationError({'job_sub_category': 'Choices limited to ' + str(limit)})
            return job_sub_category
        else:
            raise serializers.ValidationError({'job_sub_category': 'Job sub category can not be blank.'})

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
                # if 'written' not in language_data:
                #     raise serializers.ValidationError({'language_written': 'Language written proficiency is required.'})
                # if 'spoken' not in language_data:
                #     raise serializers.ValidationError({'language_spoken': 'Language spoken proficiency is required.'})
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
        job_sub_category = data.get("job_sub_category")
        if not job_category:
            raise serializers.ValidationError({'job_category': 'This field is required.'})
        if not job_sub_category:
            raise serializers.ValidationError({'job_sub_category': 'This field is required.'})
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
        JobShare.objects.create(job=job_instance)
        if language:
            for language_data in language:
                language_data = json.loads(language_data)
                language_instance = Language.objects.get(id=language_data['language'])
                job_language_instance = JobsLanguageProficiency.objects.create(
                    job=job_instance,
                    language=language_instance,
                    # spoken=language_data['spoken'],
                    # written=language_data['written']
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
    This class defines a set of fields to be updated and provides validation methods for job_category, job_sub_category, language and
    skill fields. Additionally, it handles the updating of the attachments and attachments_remove fields. It takes an
    existing instance of JobDetails and validated data, then performs the update operation on the instance.
    Attributes:
        - `job_category`: PrimaryKeyRelatedField to JobCategory model objects, many to many relationship, used to update
        job categories.
        - `job_sub_category`: PrimaryKeyRelatedField to JobSubCategory model objects, many to many relationship, used to update
        job sub categories.
        - `language`: PrimaryKeyRelatedField to Language model objects, many to many relationship, used to update
        languages.
        - `skill`: PrimaryKeyRelatedField to Skill model objects, many to many relationship, used to update skills.
        - `attachments`: ListField of file inputs, used to add new attachments to the job instance.
        - `attachments_remove`: ListField of text inputs, used to remove attachments from the job instance.
    Methods:
        - `validate_job_category`: validates the job_category field and raises a ValidationError if the value is empty
        or exceeds a specified limit.
        - `validate_job_sub_category`: validates the job_sub_category field and raises a ValidationError if the value is empty
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
    job_sub_category = serializers.PrimaryKeyRelatedField(
        queryset=JobSubCategory.objects.all(),
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
            'city', 'address', 'job_category', 'job_sub_category', 'is_full_time', 'is_part_time', 'has_contract',
            'contact_email', 'cc1', 'cc2', 'contact_whatsapp', 'highest_education', 'language', 'language_remove',
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

    def validate_job_sub_category(self, job_sub_category):
        if job_sub_category not in [None, ""]:
            limit = 3
            if len(job_sub_category) > limit:
                raise serializers.ValidationError({'job_sub_category': 'Choices limited to ' + str(limit)})
            return job_sub_category
        else:
            raise serializers.ValidationError({'job_sub_category': 'Job sub category can not be blank.'})

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
                # if 'written' not in language_data:
                #     raise serializers.ValidationError({'language_written': 'Language written proficiency is required.'})
                # if 'spoken' not in language_data:
                #     raise serializers.ValidationError({'language_spoken': 'Language spoken proficiency is required.'})
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
        job_sub_category = data.get("job_sub_category")
        if not job_category:
            raise serializers.ValidationError({'job_category': 'This field is required.'})
        if not job_sub_category:
            raise serializers.ValidationError({'job_sub_category': 'This field is required.'})
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
                        # job_language_instance.spoken = language_data['spoken']
                        # job_language_instance.written = language_data['written']
                        job_language_instance.save()
                    else:
                        job_language_instance = JobsLanguageProficiency.objects.create(
                            job=instance,
                            language=language_instance,
                            # spoken=language_data['spoken'],
                            # written=language_data['written']
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
            'start_date', 'address'
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
            'tender_category', 'tender_type', 'sector', 'tag', 'attachments', 'deadline',
            'start_date', 'attachments_remove', 'address'
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
                attachments_instance = TenderAttachmentsItem.objects.create(tender=instance,
                                                                            attachment=media_instance)
                attachments_instance.save()
        return instance


class ActivitySerializers(serializers.Serializer):
    """
    Serializer for retrieving various activity-related information for a user.

    The serializer provides information on active jobs and tenders that a user has, as well as jobs and tenders that
    the user has applied for.

    Fields:
        - `active_jobs`: The number of active jobs that the user has.
        - `active_tender`: The number of active tenders that the user has.
        - `applied_jobs`: The number of jobs that the user has applied for.
        - `applied_tender`: The number of tenders that the user has applied for.

    Methods:
        - `get_active_jobs`: Returns the number of active jobs that the user has.
        - `get_active_tender`: Returns the number of active tenders that the user has.
        - `get_applied_jobs`: Returns the number of jobs that the user has applied for.
        - `get_applied_tender`: Returns the number of tenders that the user has applied for.

    Attributes:
        - `model`: The Django User model that the serializer is based on.
        - `fields`: A list of fields to be included in the serialized representation.

    Usage:
        To use this serializer, create an instance of it and pass in a User object as the argument to the `data`
        parameter of the serializer's `__init__()` method. For example:

            user = User.objects.get(pk=1)
            serializer = ActivitySerializers(data=user)
            serialized_data = serializer.data

    """
    active_jobs = serializers.SerializerMethodField()
    active_tender = serializers.SerializerMethodField()
    applied_jobs = serializers.SerializerMethodField()
    applied_tender = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'active_jobs', 'active_tender', 'applied_jobs', 'applied_tender'
        ]

    def get_active_jobs(self, obj):
        """
        Returns the number of active jobs that the user has.

        Args:
            - `obj`: The User object for which to retrieve the number of active jobs.

        Returns:
            An integer representing the number of active jobs that the user has.
        """
        return JobDetails.objects.filter(status='active', user=obj,
                                         deadline__gte=date.today()).count()

    def get_active_tender(self, obj):
        """
        Returns the number of active tenders that the user has.

        Args:
            - `obj`: The User object for which to retrieve the number of active tenders.

        Returns:
            An integer representing the number of active tenders that the user has.
        """
        return TenderDetails.objects.filter(status='active', user=obj,
                                            deadline__gte=date.today()).count()

    def get_applied_jobs(self, obj):
        """
        Returns the number of jobs that the user has applied for.

        Args:
            - `obj`: The User object for which to retrieve the number of applied jobs.

        Returns:
            An integer representing the number of jobs that the user has applied for.
        """
        return AppliedJob.objects.filter(job__user=obj).count()

    def get_applied_tender(self, obj):
        """
        Returns the number of tenders that the user has applied for.

        Args:
            - `obj`: The User object for which to retrieve the number of applied tenders.

        Returns:
            An integer representing the number of tenders that the user has applied for.
        """
        return 0


class BlacklistedUserSerializers(serializers.ModelSerializer):
    """
    Serializer for BlackListedUser model.

    This serializer is used to serialize the BlackListedUser model and convert it into a JSON format. It includes the
    'user', 'blacklisted_user', and 'reason' fields from the BlackList model, and adds a custom field
    'blacklisted_user' using a SerializerMethodField.

    Attributes:
        blacklisted_user (serializers.SerializerMethodField): A custom field that uses a method to determine the
        serialized representation of the blacklisted_user field.

    Meta:
        model (class): The model to be serialized, which is the BlackList model.
        fields (list): A list of field names to be included in the serialized representation, which includes 'user',
        'blacklisted_user', and 'reason'.

    """

    blacklisted_user = serializers.SerializerMethodField()

    class Meta:
        model = BlackList
        fields = ['user', 'blacklisted_user', 'reason']

    def get_blacklisted_user(self, obj):
        """Get the serialized user data for a BlackList object.

        This method uses the UserSerializer to serialize the users associated with a BlackList
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A BlackList object whose user data will be serialized.

        Returns:
            A dictionary containing the serialized user data, or an empty dictionary if the
            serializer did not return any data.

        """

        context = {}
        if obj.blacklisted_user:
            get_data = UserSerializer(obj.blacklisted_user)
            if get_data.data:
                context = get_data.data
        return context


class ShareCountSerializers(serializers.ModelSerializer):
    """
    A Django REST Framework serializer for computing share counts for a user's jobs.

    This serializer computes the number of shares for a user's jobs on various platforms, including `WhatsApp`,
    `Telegram`, `Facebook`, `LinkedIn`, `email`, and `direct link`. It also computes the `total number` of shares
     across all platforms.

    Attributes:
        - `whatsapp (serializers.SerializerMethodField)`: A method field for computing the number of `WhatsApp` shares.
        - `telegram (serializers.SerializerMethodField)`: A method field for computing the number of `Telegram` shares.
        - `facebook (serializers.SerializerMethodField)`: A method field for computing the number of `Facebook` shares.
        - `linked_in (serializers.SerializerMethodField)`: A method field for computing the number of `LinkedIn` shares.
        - `mail (serializers.SerializerMethodField)`: A method field for computing the number of `email` shares.
        - `direct_link (serializers.SerializerMethodField)`: A method field for computing the number of `direct link`
            shares.
        - `total (serializers.SerializerMethodField)`: A method field for computing the `total number` of shares across
            all platforms.

    """

    whatsapp = serializers.SerializerMethodField()
    telegram = serializers.SerializerMethodField()
    facebook = serializers.SerializerMethodField()
    linked_in = serializers.SerializerMethodField()
    mail = serializers.SerializerMethodField()
    direct_link = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'whatsapp', 'telegram', 'facebook', 'linked_in',
            'mail', 'direct_link', 'total'
        ]

    def get_whatsapp(self, obj):
        """
        Computes the number of WhatsApp shares for a user's jobs.

        Args:
            obj (User): The user whose share count is being computed.

        Returns:
            int: The total number of WhatsApp shares.
        """

        job_share = JobShare.objects.filter(job__user=obj)
        whatsapp = job_share.aggregate(total_whatsapp=Sum('whatsapp'))['total_whatsapp'] or 0
        return whatsapp

    def get_telegram(self, obj):
        """
        Computes the number of Telegram shares for a user's jobs.

        Args:
            obj (User): The user whose share count is being computed.

        Returns:
            int: The total number of Telegram shares.
        """

        job_share = JobShare.objects.filter(job__user=obj)
        telegram = job_share.aggregate(total_telegram=Sum('telegram'))['total_telegram'] or 0
        return telegram

    def get_facebook(self, obj):
        """
        Computes the number of Facebook shares for a user's jobs.

        Args:
            obj (User): The user whose share count is being computed.

        Returns:
            int: The total number of Facebook shares.
        """

        job_share = JobShare.objects.filter(job__user=obj)
        facebook = job_share.aggregate(total_facebook=Sum('facebook'))['total_facebook'] or 0
        return facebook

    def get_linked_in(self, obj):
        """
        Computes the number of LinkedIn shares for a user's jobs.

        Args:
            obj (User): The user whose share count is being computed.

        Returns:
            int: The total number of LinkedIn shares.
        """

        job_share = JobShare.objects.filter(job__user=obj)
        linked_in = job_share.aggregate(total_linked_in=Sum('linked_in'))['total_linked_in'] or 0
        return linked_in

    def get_mail(self, obj):
        """
        Computes the number of email shares for a user's jobs.

        Args:
            obj (User): The user whose share count is being computed.

        Returns:
            int: The total number of email shares.
        """

        job_share = JobShare.objects.filter(job__user=obj)
        mail = job_share.aggregate(total_mail=Sum('mail'))['total_mail'] or 0
        return mail

    def get_direct_link(self, obj):
        """
        Computes the number of direct link shares for a user's jobs.

        Args:
            obj (User): The user whose share count is being computed.

        Returns:
            int: The total number of direct link shares.
        """

        job_share = JobShare.objects.filter(job__user=obj)
        direct_link = job_share.aggregate(total_direct_link=Sum('direct_link'))['total_direct_link'] or 0
        return direct_link

    def get_total(self, obj):
        """
        Return the total number of shares made by the user across different social media platforms.

        Args:
            obj: A User object for which the share counts need to be calculated.

        Returns:
            An integer representing the total number of shares made by the user.

        """

        job_share = JobShare.objects.filter(job__user=obj)
        total_counts = job_share.aggregate(
            total_whatsapp=Sum('whatsapp'),
            total_telegram=Sum('telegram'),
            total_facebook=Sum('facebook'),
            total_linked_in=Sum('linked_in'),
            total_mail=Sum('mail'),
            total_direct_link=Sum('direct_link')
        )
        return sum(total_counts.values())
