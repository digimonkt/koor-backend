from rest_framework import serializers

from job_seekers.models import (
    EducationRecord, EmploymentRecord, 
    Resume, JobSeekerLanguageProficiency, 
    JobSeekerSkill, AppliedJob,
    JobPreferences
)

from jobs.models import JobSubCategory, JobCategory
from user_profile.models import (
    JobSeekerProfile, EmployerProfile,
    UserFilters, VendorProfile
)

from project_meta.models import Media, EducationLevel

from project_meta.serializers import (
    CitySerializer, CountrySerializer, 
    SkillSerializer, ChoiceSerializer,
    TagSerializer
)

from employers.models import BlackList

from .backends import MobileOrEmailBackend as cb
from .models import User

from vendors.models import VendorSector, VendorTag, AppliedTender


class CreateUserSerializers(serializers.ModelSerializer):
    """
    CreateUserSerializer class provides serialization for creating a User model.

    The class extends the ModelSerializer from the rest_framework.serializers module. The Meta class
    specifies the model to use (User) and the fields to include in serialization.

    The validate_mobile_number method performs a custom validation on the mobile_number field. It ensures that the
    mobile_number is not blank and contains only numbers. In case of an error, it raises a ValidationError with a
    detailed error message.

    """

    class Meta:
        model = User
        fields = ['id', 'email', 'mobile_number', 'password', 'role', 'country_code']

    def validate_mobile_number(self, mobile_number):
        if mobile_number != '':
            if mobile_number.isdigit():
                try:
                    if User.objects.get(mobile_number=mobile_number):
                        raise serializers.ValidationError('mobile_number already in use.', code='mobile_number')
                except User.DoesNotExist:
                    return mobile_number
            else:
                raise serializers.ValidationError('mobile_number must contain only numbers', code='mobile_number')
        else:
            raise serializers.ValidationError('mobile_number can not be blank', code='mobile_number')

    def validate_email(self, email):
        if email != '':
            try:
                if User.objects.get(email__iexact=email):
                    raise serializers.ValidationError('email already in use.', code='email')
            except User.DoesNotExist:
                return email
        else:
            raise serializers.ValidationError('email can not be blank', code='email')

    def validate(self, data):
        country_code = data.get("country_code")
        mobile_number = data.get("mobile_number")
        email = data.get("email")
        if email in [None] and mobile_number in [None]:
            raise serializers.ValidationError({'message': 'Please enter mobile number or email.'})
        if mobile_number and country_code in ["", None]:
            raise serializers.ValidationError({'country_code': 'country code can not be blank'})
        return data


class CreateSessionSerializers(serializers.Serializer):
    """
    Serializer for creating a session for a user.

    Fields:
        email (str): The email of the user (optional).
        mobile_number (str): The mobile number of the user (optional).
        password (str): The password of the user.

    Methods:
        validate_mobile_number(mobile_number): Validates the mobile number.
        validate_email(email): Validates the email.
        validate(data): Validates the user credentials.
    """

    email = serializers.CharField(
        style={"input_type": "text"},
        write_only=True,
        required=False,
        allow_blank=True
    )
    mobile_number = serializers.CharField(
        style={"input_type": "text"},
        write_only=True,
        required=False,
        allow_blank=True
    )
    role = serializers.CharField(
        style={"input_type": "text"},
        write_only=True
    )
    password = serializers.CharField(
        style={"input_type": "text"},
        write_only=True
    )

    def validate_mobile_number(self, mobile_number):
        if mobile_number != '':
            if mobile_number.isdigit():
                try:
                    if User.objects.get(mobile_number=mobile_number):
                        return mobile_number
                except User.DoesNotExist:
                    raise serializers.ValidationError('mobile_number not exist.', code='mobile_number')
            else:
                raise serializers.ValidationError('mobile_number must contain only numbers', code='mobile_number')
        else:
            raise serializers.ValidationError('mobile_number can not be blank', code='mobile_number')

    def validate_email(self, email):
        if email != '':
            try:
                if User.objects.get(email__iexact=email):
                    return email
            except User.DoesNotExist:
                raise serializers.ValidationError('email not exist.', code='email')
        else:
            raise serializers.ValidationError('email can not be blank', code='email')

    def validate(self, data):
        email = data.get("email", "")
        mobile_number = data.get("mobile_number", "")
        role = data.get("role", "")
        password = data.get("password", "")
        user = None
        user_instance = None
        identifier = None
        if email:
            user_instance = User.objects.filter(email__iexact=email).filter(is_verified=False)
            identifier = email
        elif mobile_number:
            user_instance = User.objects.filter(mobile_number=mobile_number).filter(is_verified=False)
            identifier = mobile_number
        if user_instance.exists():
            raise serializers.ValidationError({'message': 'User not verified.'})
        else:
            user = cb.authenticate(self, identifier=identifier, password=password, role=role)
        if user:
            return user
        else:
            raise serializers.ValidationError({'message': 'Invalid login credentials.'})


class JobSeekerProfileSerializer(serializers.ModelSerializer):
    """
    JobSeekerProfileSerializer is a serializer class that serializes and deserializes the JobSeekerProfile model into
     JSON format.

    This serializer uses the Django Rest Framework's ModelSerializer class, which automatically generates fields based
    on the model.

    Attributes:
        model (JobSeekerProfile): The model that will be serialized.
        fields (tuple): The fields from the model that will be serialized.
    """
    highest_education = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    class Meta:
        model = JobSeekerProfile
        fields = (
            'gender',
            'dob',
            'employment_status',
            'description',
            'market_information_notification',
            'job_notification',
            'highest_education',
            'country',
            'city',
            'experience'
        )
    
    def get_highest_education(self, obj):
        context = {}
        if obj.highest_education:
            context['id'] = obj.highest_education.id
            context['title'] = obj.highest_education.title
            return context
        return None
    
    def get_country(self, obj):
        """Get the serialized country data for a JobFilters object.

        This method uses the CountrySerializer to serialize the country associated with a JobFilters
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A JobFilters object whose country data will be serialized.

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
        """Get the serialized city data for a JobFilters object.

        This method uses the CitySerializer to serialize the city associated with a JobFilters
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A JobFilters object whose city data will be serialized.

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


class EducationRecordSerializer(serializers.ModelSerializer):
    """
    EducationRecordSerializer is a serializer class that serializes and deserializes the EducationRecord model into
    JSON format.

    This serializer uses the Django Rest Framework's ModelSerializer class, which automatically generates fields
    based on the model.

    Attributes:
    model (EducationRecord): The model that will be serialized.
    fields (tuple): The fields from the model that will be serialized.
    """
    education_level = serializers.SerializerMethodField()
    class Meta:
        model = EducationRecord
        fields = (
            'id',
            'title',
            'start_date',
            'end_date',
            'institute',
            'education_level'
        )
        
    def get_education_level(self, obj):
        context = {}
        if obj.education_level:
            context['id'] = obj.education_level.id
            context['title'] = obj.education_level.title
            return context
        return None


class EmploymentRecordSerializer(serializers.ModelSerializer):
    """
    EmploymentRecordSerializer is a serializer class that serializes and deserializes the EmploymentRecord model into
     JSON format.

    This serializer uses the Django Rest Framework's ModelSerializer class, which automatically generates fields based
     on the model.

    Attributes:
    model (EmploymentRecord): The model that will be serialized.
    fields (tuple): The fields from the model that will be serialized.
    """

    class Meta:
        model = EmploymentRecord
        fields = (
            'id',
            'title',
            'start_date',
            'end_date',
            'organization',
            'description'
        )

class JobPreferencesSerializer(serializers.ModelSerializer):
    """
    JobPreferencesSerializer is a serializer class that serializes and deserializes the JobPreferences model into
     JSON format.

    This serializer uses the Django Rest Framework's ModelSerializer class, which automatically generates fields based
     on the model.

    Attributes:
    model (JobPreferences): The model that will be serialized.
    fields (tuple): The fields from the model that will be serialized.
    """

    class Meta:
        model = JobPreferences
        fields = (
            'id',
            'is_available',
            'display_in_search',
            'is_part_time',
            'is_full_time',
            'has_contract',
            'expected_salary',
            'pay_period'
        )


class ResumeSerializer(serializers.ModelSerializer):
    """
    ResumeSerializer is a serializer class that serializes and deserializes the Resume model into
     JSON format.

    This serializer uses the Django Rest Framework's ModelSerializer class, which automatically generates fields based
     on the model.

    Attributes:
    model (Resume): The model that will be serialized.
    fields (tuple): The fields from the model that will be serialized.
    """
    file_path = serializers.SerializerMethodField()

    class Meta:
        model = Resume
        fields = (
            'id',
            'title',
            'file_path',
            'created_at'
        )

    def get_file_path(self, obj):
        context = {}
        if obj.file_path:
            context['title'] = obj.attachment.title
            context['path'] = obj.file_path.file_path.url
            context['type'] = obj.file_path.media_type
            return context
        return None


class JobSeekerLanguageProficiencySerializer(serializers.ModelSerializer):
    """
    JobSeekerLanguageProficiencySerializer is a serializer class that serializes and deserializes the
    JobSeekerLanguageProficiency model into JSON format.

    This serializer uses the Django Rest Framework's ModelSerializer class, which automatically generates fields based
     on the model.

    Attributes:
    model (JobSeekerLanguageProficiency): The model that will be serialized.
    fields (tuple): The fields from the model that will be serialized.
    """
    language = serializers.SerializerMethodField()
    class Meta:
        model = JobSeekerLanguageProficiency
        fields = (
            'id',
            'language',
            'written',
            'spoken'
        )
    
    def get_language(self, obj):
        context = {}
        if obj.language:
            context['id'] = obj.language.id
            context['title'] = obj.language.title
            return context
        return None


class JobSeekerSkillSerializer(serializers.ModelSerializer):
    """
    JobSeekerSkillSerializer is a serializer class that serializes and deserializes the JobSeekerSkill model into JSON
    format.

    This serializer uses the Django Rest Framework's ModelSerializer class, which automatically generates fields based
     on the model.

    Attributes:
    model (JobSeekerSkill): The model that will be serialized.
    fields (tuple): The fields from the model that will be serialized.
    """
    skill = serializers.SerializerMethodField()
    class Meta:
        model = JobSeekerSkill
        fields = (
            'id',
            'skill'
        )
        
    def get_skill(self, obj):
        context = {}
        get_data = SkillSerializer(obj.skill)
        if get_data.data:
            context = get_data.data
        return context


class JobSeekerDetailSerializers(serializers.ModelSerializer):
    """
    JobSeekerDetailSerializers

    A class-based serializer for the User model. The serializer includes various fields such as profile,
    education_record, work_experience, resume, languages, and skills. These fields are serialized using the
    SerializerMethodField and are populated by the get_* methods defined in the class.

    The fields returned by the serializer include:

        - id: the primary key of the User model
        - email: the email address of the user
        - mobile_number: the mobile number of the user
        - country_code: the country code of the user
        - name: the display name of the user
        - image: the image of the user
        - role: the role of the user
        - profile: the profile of the job seeker
        - education_record: the education record of the job seeker
        - work_experience: the work experience of the job seeker
        - resume: the resume of the job seeker
        - languages: the languages spoken by the job seeker
        - skills: the skills of the job seeker

    Methods:

        - get_profile(self, obj): returns the profile of the job seeker
        - get_education_record(self, obj): returns the education record of the job seeker
        - get_work_experience(self, obj): returns the work experience of the job seeker
        - get_resume(self, obj): returns the resume of the job seeker
        - get_languages(self, obj): returns the languages spoken by the job seeker
        - get_skills(self, obj): returns the skills of the job seeker
    """

    profile = serializers.SerializerMethodField()
    education_record = serializers.SerializerMethodField()
    work_experience = serializers.SerializerMethodField()
    job_preferences = serializers.SerializerMethodField()
    resume = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()
    skills = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    profile_completed = serializers.SerializerMethodField()
    ready_for_chat = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'mobile_number', 'country_code', 'name', 'image', 'role', 'profile',
            'education_record', 'work_experience', 'resume', 'languages', 'skills', 'job_preferences',
            'is_online', 'profile_completed', 'ready_for_chat'
        ]
        
    
    def get_ready_for_chat(self, obj):
    
        ready_for_chat_record = False
        if 'user' in self.context:
            user = self.context['user']
            if self.context['user'].is_authenticated:
                ready_for_chat_record = AppliedJob.objects.filter(
                    job__user=user,
                    user=obj
                ).exists()
        return ready_for_chat_record

    def get_profile_completed(self, obj):
        context = False
        if obj.name and obj.user_profile_jobseekerprofile_user.gender and obj.user_profile_jobseekerprofile_user.experience and obj.user_profile_jobseekerprofile_user.dob and obj.user_profile_jobseekerprofile_user.employment_status and obj.user_profile_jobseekerprofile_user.country and obj.user_profile_jobseekerprofile_user.city and obj.user_profile_jobseekerprofile_user.highest_education:
            if JobSeekerSkill.objects.filter(user=obj).exists():
                context = True
        return context
    
    def get_image(self, obj):
        context = dict()
        if obj.image:
            context['id'] = obj.image.id
            if obj.image.title == "profile image":
                context['path'] = str(obj.image.file_path)
            else:
                context['path'] = obj.image.file_path.url
            context['title'] = obj.image.title
        return context
    
    def get_profile(self, obj):
        context = dict()
        try:
            user_data = JobSeekerProfile.objects.get(user=obj)
            get_data = JobSeekerProfileSerializer(user_data)
            if get_data.data:
                context = get_data.data
        except JobSeekerProfile.DoesNotExist:
            pass
        finally:
            return context

    def get_education_record(self, obj):
        context = []
        education_data = EducationRecord.objects.filter(user=obj)
        get_data = EducationRecordSerializer(education_data, many=True)
        if get_data.data:
            context = get_data.data
        return context
    
    def get_job_preferences(self, obj):
        context = []
        try:
            job_preferences_data = JobPreferences.objects.get(user=obj)
            get_data = JobPreferencesSerializer(job_preferences_data)
            if get_data.data:
                context = get_data.data
        except JobPreferences.DoesNotExist:
            pass
        finally:
            return context

    def get_work_experience(self, obj):
        context = []
        employment_data = EmploymentRecord.objects.filter(user=obj)
        get_data = EmploymentRecordSerializer(employment_data, many=True)
        if get_data.data:
            context = get_data.data
        return context

    def get_resume(self, obj):
        context = []
        resume_data = Resume.objects.filter(user=obj)
        get_data = ResumeSerializer(resume_data, many=True)
        if get_data.data:
            context = get_data.data
        return context

    def get_languages(self, obj):
        context = []
        languages_data = JobSeekerLanguageProficiency.objects.filter(user=obj)
        get_data = JobSeekerLanguageProficiencySerializer(languages_data, many=True)
        if get_data.data:
            context = get_data.data
        return context

    def get_skills(self, obj):
        context = []
        skills_data = JobSeekerSkill.objects.filter(user=obj)
        get_data = JobSeekerSkillSerializer(skills_data, many=True)
        if get_data.data:
            context = get_data.data
        return context


class EmployerProfileSerializer(serializers.ModelSerializer):
    """
    EmployerProfileSerializer is a serializer class that serializes and deserializes the EmployerProfile model into JSON
    format.

    This serializer uses the Django Rest Framework's ModelSerializer class, which automatically generates fields based
     on the model.

    Attributes:
    model (EmployerProfile): The model that will be serialized.
    fields (tuple): The fields from the model that will be serialized.
    """
    license_id_file = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    organization_type = serializers.SerializerMethodField()

    class Meta:
        model = EmployerProfile
        fields = (
            'description',
            'organization_type',
            'market_information_notification',
            'other_notification',
            'license_id',
            'license_id_file',
            'is_verified',
            'description',
            'address',
            'website',
            'country',
            'city',
            'is_verified',
            'points'
        )

    def get_license_id_file(self, obj):
        context = {}
        if obj.license_id_file:
            context['id'] = obj.license_id_file.id
            context['title'] = obj.license_id_file.title
            context['path'] = obj.license_id_file.file_path.url
            context['type'] = obj.license_id_file.media_type
            return context
        return None
    
    def get_country(self, obj):
        """
        Retrieves the serialized data for the country related to a JobDetails object.

        Args:
            obj: The JobDetails object to retrieve the country data for.

        Returns:
            A dictionary containing the serialized country data.

        """

        context = {}
        if obj.country:
            get_data = CountrySerializer(obj.country)
            if get_data.data:
                context = get_data.data
        return context

    def get_city(self, obj):
        """
        Retrieves the serialized data for the city related to a JobDetails object.

        Args:
            obj: The JobDetails object to retrieve the city data for.

        Returns:
            A dictionary containing the serialized city data.

        """

        context = {}
        if obj.city:
            get_data = CitySerializer(obj.city)
            if get_data.data:
                context = get_data.data
        return context

    def get_organization_type(self, obj):
        """
        Retrieves the serialized data for the organization type related to a JobDetails object.

        Args:
            obj: The JobDetails object to retrieve the organization type data for.

        Returns:
            A dictionary containing the serialized organization type data.

        """

        context = {}
        if obj.organization_type:
            get_data = ChoiceSerializer(obj.organization_type, many=True)
            if get_data.data:
                context = get_data.data[0]
        return context



class EmployerDetailSerializers(serializers.ModelSerializer):
    """
    Serializer class for Employer Detail

    Serializes and deserializes employer detail data from/to python objects and JSON format.
    The fields are defined in the 'Meta' class and correspond to the User model.

    Attributes:
        serializers (Module): The serializers module from the Django REST framework.
        ModelSerializer (class): The base serializer class from the Django REST framework.

    Methods:
        get_profile(self, obj):
            Returns employer profile data serialized into JSON format

    """

    profile = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'mobile_number', 'country_code', 
            'name', 'image', 'role', 'get_email', 
            'get_notification', 'profile', 'is_online'
        ]
        
    def get_image(self, obj):
        context = dict()
        if obj.image:
            context['id'] = obj.image.id
            if obj.image.title == "profile image":
                context['path'] = str(obj.image.file_path)
            else:
                context['path'] = obj.image.file_path.url
            context['title'] = obj.image.title
        return context

    def get_profile(self, obj):
        context = dict()
        try:
            user_data = EmployerProfile.objects.get(user=obj)
            get_data = EmployerProfileSerializer(user_data)
            if get_data.data:
                context = get_data.data
        except EmployerProfile.DoesNotExist:
            pass
        finally:
            return context


class VendorSectorSerializer(serializers.ModelSerializer):
    """
    Serializer for VendorSector model, used to serialize and deserialize data.

    Attributes:
        sector (SerializerMethodField): Field representing the sector.

    Meta:
        model (VendorSector): Model class associated with the serializer.
        fields (tuple): Fields to include in the serialized representation.
            - id: VendorSector ID
            - sector: Serialized representation of the sector

    Methods:
        get_sector(obj): Method to retrieve the serialized data for the sector field.

    Example usage:
        serializer = VendorSectorSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            serialized_data = serializer.data
        else:
            errors = serializer.errors
    """

    sector = serializers.SerializerMethodField()
    class Meta:
        model = VendorSector
        fields = (
            'id',
            'sector'
        )
        
    def get_sector(self, obj):
        """
        Retrieve the serialized data for the sector field.

        Args:
            obj: The VendorSector instance to serialize.

        Returns:
            dict: Serialized representation of the sector.

        Example:
            serializer = VendorSectorSerializer()
            sector_data = serializer.get_sector(vendor_sector_instance)
        """
        
        context = {}
        get_data = ChoiceSerializer(obj.sector)
        if get_data.data:
            context = get_data.data
        return context


class VendorTagSerializer(serializers.ModelSerializer):
    """
    Serializer for VendorTag model, used to serialize and deserialize data.

    Attributes:
        tag (SerializerMethodField): Field representing the tag.

    Meta:
        model (VendorTag): Model class associated with the serializer.
        fields (tuple): Fields to include in the serialized representation.
            - id: VendorTag ID
            - tag: Serialized representation of the tag

    Methods:
        get_tag(obj): Method to retrieve the serialized data for the tag field.

    Example usage:
        serializer = VendorTagSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            serialized_data = serializer.data
        else:
            errors = serializer.errors
    """

    tag = serializers.SerializerMethodField()
    class Meta:
        model = VendorTag
        fields = (
            'id',
            'tag'
        )
        
    def get_tag(self, obj):
        """
        Retrieve the serialized data for the tag field.

        Args:
            obj: The VendorTag instance to serialize.

        Returns:
            dict: Serialized representation of the tag.

        Example:
            serializer = VendorTagSerializer()
            tag_data = serializer.get_tag(vendor_tag_instance)
        """
        
        context = {}
        get_data = TagSerializer(obj.tag)
        if get_data.data:
            context = get_data.data
        return context


class VendorProfileSerializer(serializers.ModelSerializer):
    """
    VendorProfileSerializer is a serializer class that serializes and deserializes the VendorProfile model into JSON
    format.

    This serializer uses the Django Rest Framework's ModelSerializer class, which automatically generates fields based
     on the model.

    Attributes:
    model (VendorProfile): The model that will be serialized.
    fields (tuple): The fields from the model that will be serialized.
    """
    license_id_file = serializers.SerializerMethodField()
    registration_certificate = serializers.SerializerMethodField()
    organization_type = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()

    class Meta:
        model = VendorProfile
        fields = (
            'description',
            'organization_type',
            'license_id',
            'license_id_file',
            'registration_number',
            'registration_certificate',
            'operating_years',
            'jobs_experience',
            'website',
            'market_information_notification',
            'other_notification',
            'address',
            'country',
            'city'
        )

    def get_organization_type(self, obj):
        """
        Retrieves the serialized data for the organization type related to a JobDetails object.

        Args:
            obj: The JobDetails object to retrieve the organization type data for.

        Returns:
            A dictionary containing the serialized organization type data.

        """

        context = {}
        if obj.organization_type:
            get_data = ChoiceSerializer(obj.organization_type, many=True)
            if get_data.data:
                context = get_data.data[0]
        return context
    
    def get_license_id_file(self, obj):
        context = {}
        if obj.license_id_file:
            context['id'] = obj.license_id_file.id
            context['title'] = obj.license_id_file.title
            context['path'] = obj.license_id_file.file_path.url
            context['type'] = obj.license_id_file.media_type
            return context
        return None
    
    def get_registration_certificate(self, obj):
        context = {}
        if obj.registration_certificate:
            context['id'] = obj.registration_certificate.id
            context['title'] = obj.registration_certificate.title
            context['path'] = obj.registration_certificate.file_path.url
            context['type'] = obj.registration_certificate.media_type
            return context
        return None
    
    def get_country(self, obj):
        """
        Retrieves the serialized data for the country related to a JobDetails object.

        Args:
            obj: The JobDetails object to retrieve the country data for.

        Returns:
            A dictionary containing the serialized country data.

        """

        context = {}
        if obj.country:
            get_data = CountrySerializer(obj.country)
            if get_data.data:
                context = get_data.data
        return context

    def get_city(self, obj):
        """
        Retrieves the serialized data for the city related to a JobDetails object.

        Args:
            obj: The JobDetails object to retrieve the city data for.

        Returns:
            A dictionary containing the serialized city data.

        """

        context = {}
        if obj.city:
            get_data = CitySerializer(obj.city)
            if get_data.data:
                context = get_data.data
        return context


class VendorDetailSerializers(serializers.ModelSerializer):
    """
    Serializer class for Vendor Detail

    Serializes and deserializes vendor detail data from/to python objects and JSON format.
    The fields are defined in the 'Meta' class and correspond to the User model.

    Attributes:
        serializers (Module): The serializers module from the Django REST framework.
        ModelSerializer (class): The base serializer class from the Django REST framework.

    Methods:
        get_profile(self, obj):
            Returns vendor profile data serialized into JSON format

    """

    profile = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    sector = serializers.SerializerMethodField()
    tag = serializers.SerializerMethodField()
    ready_for_chat = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'mobile_number', 'country_code', 
            'name', 'image', 'role', 'get_email', 'get_notification', 
            'profile', 'sector', 'tag', 'is_online', 'ready_for_chat'
        ]
        
    
    def get_ready_for_chat(self, obj):
    
        ready_for_chat_record = False
        if 'user' in self.context:
            user = self.context['user']
            if self.context['user'].is_authenticated:
                ready_for_chat_record = AppliedTender.objects.filter(
                    tender__user=user,
                    user=obj
                ).exists()
        return ready_for_chat_record
        
    def get_image(self, obj):
        context = dict()
        if obj.image:
            context['id'] = obj.image.id
            if obj.image.title == "profile image":
                context['path'] = str(obj.image.file_path)
            else:
                context['path'] = obj.image.file_path.url
            context['title'] = obj.image.title
        return context

    def get_profile(self, obj):
        context = dict()
        try:
            user_data = VendorProfile.objects.get(user=obj)
            get_data = VendorProfileSerializer(user_data)
            if get_data.data:
                context = get_data.data
        except VendorProfile.DoesNotExist:
            pass
        finally:
            return context

    def get_sector(self, obj):
        """
        Retrieves the sector data associated with the given object's user.

        Parameters:
            obj: An object containing user information.

        Returns:
            A list of sector data retrieved from the VendorSector model associated with the user.
        """
        
        context = []
        sector_data = VendorSector.objects.filter(user=obj)
        get_data = VendorSectorSerializer(sector_data, many=True)
        if get_data.data:
            context = get_data.data
        return context

    def get_tag(self, obj):
        """
        Retrieves the tag data associated with the given object's user.

        Parameters:
            obj: An object containing user information.

        Returns:
            A list of tag data retrieved from the VendorTag model associated with the user.
        """
        
        context = []
        tag_data = VendorTag.objects.filter(user=obj)
        get_data = VendorTagSerializer(tag_data, many=True)
        if get_data.data:
            context = get_data.data
        return context


class UpdateImageSerializers(serializers.ModelSerializer):
    """
    Serializer class for `updating a user's profile image`.

    Attributes:
        - `profile_image (FileField)`: A file field that represents the user's new profile image.
    """
    profile_image = serializers.FileField(
        style={"input_type": "file"},
        write_only=True,
        allow_null=False
    )

    class Meta:
        model = User
        fields = ['id', 'profile_image']

    def validate_profile_image(self, profile_image):
        """
        Validates that the uploaded profile image is a valid image file.

        Args:
            - `profile_image (File)`: The profile image file to validate.

        Returns:
            - `File`: The validated profile image file.

        Raises:
            - `ValidationError`: If the profile image file is `blank or invalid`.
        """
        if profile_image in ["", None]:
            raise serializers.ValidationError('Profile image can not be blank.', code='profile_image')
        content_type = str(profile_image.content_type).split("/")
        if content_type[0] == "image":
            return profile_image
        else:
            raise serializers.ValidationError('Invalid profile image.', code='profile_image')

    def update(self, instance, validated_data):
        """
        Updates the user's profile image.

        Args:
            - `instance (User)`: The User instance to update.
            - `validated_data (dict)`: The validated data containing the new profile image.

        Returns:
            - `User`: The updated `User` instance.
        """
        super().update(instance, validated_data)
        if 'profile_image' in validated_data:
            # Get media type from upload license file
            content_type = str(validated_data['profile_image'].content_type).split("/")
            if content_type[0] not in ["video", "image"]:
                media_type = 'document'
            else:
                media_type = content_type[0]
            # save media file into media table and get instance of saved data.
            media_instance = Media(title=validated_data['profile_image'].name,
                                   file_path=validated_data['profile_image'], media_type=media_type)
            media_instance.save()
            # save media instance into license id file into employer profile table.
            instance.image = media_instance
            instance.save()
        return instance


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
    description = serializers.SerializerMethodField()
    is_blacklisted = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'email',
            'country_code',
            'mobile_number',
            'image',
            'description',
            'is_blacklisted',
            'is_online'
        )

    def get_image(self, obj):
        context = {}
        if obj.image:
            context['id'] = obj.image.id
            context['title'] = obj.image.title
            if obj.image.title == "profile image":
                context['path'] = str(obj.image.file_path)
            else:
                context['path'] = obj.image.file_path.url
            context['type'] = obj.image.media_type
            return context
        return None
    
    def get_description(self, obj):
        context = {}
        if obj.role == 'job_seeker':
            if JobSeekerProfile.objects.filter(user=obj).exists():
                jobseeker_data = JobSeekerProfile.objects.get(user=obj)
                return jobseeker_data.description
        return None
    
    def get_is_blacklisted(self, obj):
        is_blacklisted_record = False
        is_blacklisted_record = BlackList.objects.filter(
            blacklisted_user=obj
        ).exists()
        return is_blacklisted_record

class ApplicantDetailSerializers(serializers.ModelSerializer):
    """
    ApplicantDetailSerializers

    A class-based serializer for the User model. The serializer includes various fields such as profile,
    education_record, work_experience, resume, languages, and skills. These fields are serialized using the
    SerializerMethodField and are populated by the get_* methods defined in the class.

    The fields returned by the serializer include:

        - id: the primary key of the User model
        - name: the display name of the user
        - education_record: the education record of the job seeker
        - work_experience: the work experience of the job seeker
        - languages: the languages spoken by the job seeker
        - skills: the skills of the job seeker
        - description: the description of the job seeker
        - image: the image of the user

    Methods:

        - get_education_record(self, obj): returns the education record of the job seeker
        - get_work_experience(self, obj): returns the work experience of the job seeker
        - get_languages(self, obj): returns the languages spoken by the job seeker
        - get_skills(self, obj): returns the skills of the job seeker
        - get_description(self, obj): returns the description of the job seeker
        - `get_image(obj)`: A method that takes a User instance and returns the URL of the user's image if it exists,
            otherwise None.
    """

    education_record = serializers.SerializerMethodField()
    work_experience = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()
    skills = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    is_blacklisted = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'description', 'image', 'education_record', 'work_experience', 
                  'languages', 'skills', 'is_blacklisted', 'country', 'city', 'is_online']
    
    def get_image(self, obj):
        context = {}
        if obj.image:
            context['id'] = obj.image.id
            context['title'] = obj.image.title
            if obj.image.title == "profile image":
                context['path'] = str(obj.image.file_path)
            else:
                context['path'] = obj.image.file_path.url
            context['type'] = obj.image.media_type
            return context
        return None
    
    def get_is_blacklisted(self, obj):
        is_blacklisted_record = False
        is_blacklisted_record = BlackList.objects.filter(
            blacklisted_user=obj
        ).exists()
        return is_blacklisted_record
    
    def get_description(self, obj):
        context = {}
        if obj.role == 'job_seeker':
            try:
                jobseeker_data = JobSeekerProfile.objects.get(user=obj)
                return jobseeker_data.description
            except JobSeekerProfile.DoesNotExist:
                pass  
        return None

    def get_education_record(self, obj):
        context = []
        education_data = EducationRecord.objects.filter(user=obj)
        get_data = EducationRecordSerializer(education_data, many=True)
        if get_data.data:
            context = get_data.data
        return context

    def get_work_experience(self, obj):
        context = []
        employment_data = EmploymentRecord.objects.filter(user=obj)
        get_data = EmploymentRecordSerializer(employment_data, many=True)
        if get_data.data:
            context = get_data.data
        return context

    def get_languages(self, obj):
        context = []
        languages_data = JobSeekerLanguageProficiency.objects.filter(user=obj)
        get_data = JobSeekerLanguageProficiencySerializer(languages_data, many=True)
        if get_data.data:
            context = get_data.data
        return context

    def get_skills(self, obj):
        context = []
        skills_data = JobSeekerSkill.objects.filter(user=obj)
        get_data = JobSeekerSkillSerializer(skills_data, many=True)
        if get_data.data:
            context = get_data.data
        return context
    
    def get_country(self, obj):
        context = {}
        if obj.role == 'job_seeker':
            try:
                jobseeker_data = JobSeekerProfile.objects.get(user=obj)
                if jobseeker_data.country:
                    return jobseeker_data.country.title
            except JobSeekerProfile.DoesNotExist:
                pass 
        return None
    
    def get_city(self, obj):
        context = {}
        if obj.role == 'job_seeker':
            try:
                jobseeker_data = JobSeekerProfile.objects.get(user=obj)
                if jobseeker_data.city:
                    return jobseeker_data.city.title
            except JobSeekerProfile.DoesNotExist:
                pass 
        return None


class SocialLoginSerializers(serializers.ModelSerializer):
    """
    SocialLoginSerializers is a serializer class for the User model that creates social login serializers.

    The class contains three methods: `validate_mobile_number`, `validate_email`, and `validate`.

    `validate_mobile_number` validates that the mobile number is not blank and contains only numbers. It raises a
    `serializers.ValidationError` if the mobile number is blank or contains non-numeric characters.

    `validate_email` validates that the email is not blank. It raises a `serializers.ValidationError` if the email is
    blank.

    `validate` validates that the source is not blank and that the country code is not blank if the mobile number is
    present. It returns the validated data.

    Parameters:
        - `serializers.ModelSerializer`: A ModelSerializer object that defines the serialization of the User model.

    Returns:
        - `dict`: A dictionary containing the validated data.

    Raises:
        - `serializers.ValidationError`: If the mobile number is blank or contains non-numeric characters, or if the
        email is blank, or if the source is blank or the country code is blank when the mobile number is present.
    """
    display_image = serializers.CharField(
        style={"input_type": "text"},
        write_only=True,
        allow_blank=False,
        required=False
    )
    class Meta:
        model = User
        fields = ['id', 'social_login_id', 'email', 'mobile_number', 'source', 'name', 'role', 'country_code', 'display_image', 'is_online']

    def validate_mobile_number(self, mobile_number):
        if mobile_number != '':
            if mobile_number.isdigit():
                return mobile_number
            else:
                raise serializers.ValidationError('mobile_number must contain only numbers', code='mobile_number')
        else:
            raise serializers.ValidationError('mobile_number can not be blank', code='mobile_number')

    def validate_email(self, email):
        if email != '':
            return email
        else:
            raise serializers.ValidationError('email can not be blank', code='email')
        
    def validate_display_image(self, display_image):
        if display_image != '':
            return display_image
        else:
            raise serializers.ValidationError('display image can not be blank', code='display_image')

    def validate(self, data):
        country_code = data.get("country_code")
        mobile_number = data.get("mobile_number")
        source = data.get("source")
        if source in ["", None]:
            raise serializers.ValidationError({'source': 'source can not be blank'})
        if mobile_number and country_code in ["", None]:
            raise serializers.ValidationError({'country_code': 'country code can not be blank'})
        return data

    def save(self):
        display_image = None
        if 'display_image' in self.validated_data:
            display_image = self.validated_data.pop('display_image')
        user_instance = super().save(is_verified=True)
        if display_image:
            media_instance = Media(title="profile image", file_path=display_image, media_type="image")
            media_instance.save()
            user_instance.image = media_instance
            user_instance.save()
        return self
    

class UserFiltersSerializers(serializers.ModelSerializer):
    """
    UserFiltersSerializers is a class-based serializer that inherits from the ModelSerializer class of the Django REST
    Framework.
    It defines a Meta class that specifies the UserFilters model and the fields to be included in the serialization.

    Attributes:
        - `model (class)`: The Django model class that this serializer is based on.
        - `fields (list)`: A list of fields to be included in the serialized output.
        
    Usage:
        - This serializer can be used to serialize UserFilters objects and convert them to JSON format for use in HTTP
        requests and responses.
    """

    class Meta:
        model = UserFilters
        fields = [
            'id', 'role', 'title', 'country', 'city', 'category', 'sub_category',
            'is_full_time', 'is_part_time', 'has_contract', 'is_notification',
            'salary_min', 'salary_max', 'availability', 'experience', 
            'organization_type', 'sector', 'tag', 'years_in_market'
        ]
   
    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        return instance


class UserCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the `JobSubCategory` model.

    Meta:
        - `model (JobSubCategory)`: The model that the serializer is based on.
        - `fields (list)`: The fields to include in the serialized output.

    """

    class Meta:
        model = JobCategory
        fields = ['id', 'title']

class UserSubCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the `JobSubCategory` model.

    Meta:
        - `model (JobSubCategory)`: The model that the serializer is based on.
        - `fields (list)`: The fields to include in the serialized output.

    """

    class Meta:
        model = JobSubCategory
        fields = ['id', 'title']


class GetUserFiltersSerializers(serializers.ModelSerializer):
    """
    A serializer class to convert `UserFilters` model instances into Python objects that can be easily rendered into
    JSON format.

    The serializer returns a serialized representation of the model fields specified in the 'Meta' class, along with
    additional fields generated by the `SerializerMethodField()` methods.

    Attributes:
        - `country (serializers.SerializerMethodField())`: A SerializerMethodField() method to generate the `country`
            field for the serialized representation.
        - `city (serializers.SerializerMethodField())`: A SerializerMethodField() method to generate the `city` field
            for the serialized representation.
        - `category (serializers.SerializerMethodField())`: A SerializerMethodField() method to generate the `category`
            field for the serialized representation.

    Meta:
        - `model (UserFilters)`: The model that this serializer class is based on.
        - `fields (list)`: A list of strings representing the fields to be serialized, in the order they should appear.

    Returns:
        - A serialized representation of UserFilters model instances, along with additional fields generated by the
            `SerializerMethodField()` methods.

    """

    country = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    sub_category = serializers.SerializerMethodField()
    organization_type = serializers.SerializerMethodField()
    sector = serializers.SerializerMethodField()
    tag = serializers.SerializerMethodField()

    class Meta:
        model = UserFilters
        fields = [
            'id', 'role', 'title', 'country', 'city', 'category', 'sub_category',
            'is_full_time', 'is_part_time', 'has_contract', 'is_notification',
            'salary_min', 'salary_max', 'availability', 'experience', 
            'organization_type', 'sector', 'tag', 'years_in_market'
        ]

    def get_country(self, obj):
        """Get the serialized country data for a JobFilters object.

        This method uses the CountrySerializer to serialize the country associated with a JobFilters
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A JobFilters object whose country data will be serialized.

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
        """Get the serialized city data for a JobFilters object.

        This method uses the CitySerializer to serialize the city associated with a JobFilters
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A JobFilters object whose city data will be serialized.

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

    def get_category(self, obj):
        """Get the serialized category data for a UserFilters object.

        This method uses the UserCategorySerializer to serialize the categories associated with a UserFilters
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A UserFilters object whose category data will be serialized.

        Returns:
            A dictionary containing the serialized job category data, or an empty dictionary if the
            serializer did not return any data.

        """

        context = []
        get_data = UserCategorySerializer(obj.category, many=True)
        if get_data.data:
            context = get_data.data
        return context
    
    def get_sub_category(self, obj):
        """Get the serialized sub category data for a UserFilters object.

        This method uses the UserSubCategorySerializer to serialize the categories associated with a UserFilters
        object. If the serializer returns data, it is assigned to a dictionary and returned.

        Args:
            obj: A UserFilters object whose sub category data will be serialized.

        Returns:
            A dictionary containing the serialized job category data, or an empty dictionary if the
            serializer did not return any data.

        """

        context = []
        get_data = UserSubCategorySerializer(obj.sub_category, many=True)
        if get_data.data:
            context = get_data.data
        return context
    
    def get_organization_type(self, obj):
        
        context = []
        get_data = ChoiceSerializer(obj.organization_type, many=True)
        if get_data.data:
            context = get_data.data
        return context
    
    def get_sector(self, obj):
        
        context = []
        get_data = ChoiceSerializer(obj.sector, many=True)
        if get_data.data:
            context = get_data.data
        return context
    
    def get_tag(self, obj):
        
        context = []
        get_data = TagSerializer(obj.tag, many=True)
        if get_data.data:
            context = get_data.data
        return context


class SearchUserSerializers(serializers.ModelSerializer):
    """
    Serializer class for the `User` model.

    The `SearchUserSerializers` class extends `serializers.ModelSerializer` and is used to create instances of the
    `User` model. It defines the fields that should be included in the serialized representation of the model,
    including 'id', 'role', 'name', 'email', 'image', 'description', 'skills', 'highest_education', 'country', 'city'.
    """
    image = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    skills = serializers.SerializerMethodField()
    highest_education = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'role', 'name', 'email', 'image', 
                  'description', 'skills','country', 'city', 
                  'highest_education', 'is_online'
                  ]

    def get_image(self, obj):
        context = {}
        if obj.image:
            context['id'] = obj.image.id
            context['title'] = obj.image.title
            if obj.image.title == "profile image":
                context['path'] = str(obj.image.file_path)
            else:
                context['path'] = obj.image.file_path.url
            context['type'] = obj.image.media_type
            return context
        return None
    
    def get_description(self, obj):
        context = {}
        if obj.role == 'job_seeker':
            try:
                jobseeker_data = JobSeekerProfile.objects.get(user=obj)
                return jobseeker_data.description
            except JobSeekerProfile.DoesNotExist:
                pass            
        elif obj.role == 'vendor':
            try:
                vendor_data = VendorProfile.objects.get(user=obj)
                return vendor_data.description
            except VendorProfile.DoesNotExist:
                pass 
        return None    
    
    def get_highest_education(self, obj):
        context = {}
        if obj.role == 'job_seeker':
            try:
                jobseeker_data = JobSeekerProfile.objects.get(user=obj)
                if jobseeker_data.highest_education:
                    return jobseeker_data.highest_education.title
            except JobSeekerProfile.DoesNotExist:
                pass 
        return None
    
    def get_country(self, obj):
        context = {}
        if obj.role == 'job_seeker':
            try:
                jobseeker_data = JobSeekerProfile.objects.get(user=obj)
                if jobseeker_data.country:
                    return jobseeker_data.country.title
            except JobSeekerProfile.DoesNotExist:
                pass 
        return None
    
    def get_city(self, obj):
        context = {}
        if obj.role == 'job_seeker':
            try:
                jobseeker_data = JobSeekerProfile.objects.get(user=obj)
                if jobseeker_data.city:
                    return jobseeker_data.city.title
            except JobSeekerProfile.DoesNotExist:
                pass 
        return None
    
    def get_skills(self, obj):
        context = []
        if obj.role == 'job_seeker':
            try:
                skills_data = JobSeekerSkill.objects.filter(user=obj)
                get_data = JobSeekerSkillSerializer(skills_data, many=True)
                if get_data.data:
                    context = get_data.data
                return context
            except JobSeekerSkill.DoesNotExist:
                pass 
        return None

