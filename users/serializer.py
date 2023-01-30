# IMPORT PYTHON PACKAGE.
from rest_framework import exceptions, status
from rest_framework import serializers

from core.utils import CustomValidationError

# IMPORT SOME IMPORTANT FUNCTION AND DATA
from user_profile.models import JobSeekerProfile, EmployerProfile

# IMPORT SOME IMPORTANT FUNCTION AND DATA
from user_profile.models import JobSeekerProfile
from job_seeker.models import EducationRecord, EmploymentRecord, Resume, JobSeekerLanguageProficiency, JobSeekerSkill

# IMPORT CUSTOM AUTHENTICATE FUNCTION FORM BACKENDS.PY FILE.
from .backends import MobileOrEmailBackend as cb

# IMPORT SOME MODEL CLASS FROM SOME APP'S MODELS.PY FILE.
from .models import User


class CreateUserSerializers(serializers.ModelSerializer):
    """
    Created a serializer class for create user. Here we use ModelSerializer, using User model.
    Here we create some validation like:
        email or mobile_number is required.
        password is required.
        checked email or mobile_number is already exist or not.
    After create user return user instance.
    """

    class Meta:
        model = User
        fields = ['email', 'mobile_number', 'password', 'role', 'country_code']

    # CREATE A VALIDATION FUNCTION FOR INSERT USER RECORD INTO USER TABLE.
    def validate(self, data):
        email = data.get("email", "")
        mobile_number = data.get("mobile_number", "")
        password = data.get("password", "")
        role = data.get("role", "")
        country_code = data.get("country_code", "")
        if email:
            if User.objects.filter(email=email).exists():  # CHECK EMAIL ALREADY REGISTERED OR NOT.
                mes = "Email already exist."  # MESSAGE IF USER ALREADY REGISTERED.
                raise CustomValidationError(
                    mes,
                    'email',
                    status.HTTP_400_BAD_REQUEST
                )  # CALL MESSAGE IF USER ALREADY REGISTERED.
        if mobile_number:
            if mobile_number.isnumeric():
                # CHECK MOBILE NUMBER ALREADY REGISTERED OR NOT.
                if User.objects.filter(mobile_number=mobile_number).exists():
                    mes = "Mobile number already exist."  # MESSAGE IF USER ALREADY REGISTERED.
                    raise CustomValidationError(
                        mes,
                        'mobile_number',
                        status.HTTP_400_BAD_REQUEST
                    )  # CALL MESSAGE IF USER ALREADY REGISTERED.
            else:
                mes = "Invalid mobile number."  # MESSAGE IF USER ALREADY REGISTERED.
                raise CustomValidationError(
                    mes,
                    'mobile_number',
                    status.HTTP_400_BAD_REQUEST
                )  # CALL MESSAGE IF USER ALREADY REGISTERED.

        if email or mobile_number:
            try:
                user_data = User(
                    email=email,
                    mobile_number=mobile_number,
                    country_code=country_code,
                    is_active=True,
                    role=role
                )  # SET DATA INTO USER TABLE FOR CRATE USER BUT USER NOT CREATED AT THAT MOMENT.
                user_data.set_password(password)  # SET PASSWORD FOR USER.

                user_data.save()  # SAVE USER DATA INTO TABLE.
                return user_data  # RETURN SOME INFORMATION ACCORDING TO FUNCTION.
            except Exception as e:
                raise exceptions.APIException(e)  # CALL MESSAGE IF USER NOT REGISTERED.
        else:
            # MESSAGE IF EMAIL AND MOBILE NUMBER BOTH FIELD ARE BLANK.
            mes = "Mobile number or Email is required for user registration."
            raise CustomValidationError(
                mes,
                'email',
                status.HTTP_400_BAD_REQUEST
            )  # CALL MESSAGE IF USER ALREADY REGISTERED.


class CreateSessionSerializers(serializers.Serializer):
    """
    Created a serializer class for user authentication. Here we use Serializer.
    Here we create some validation like:
        email or mobile_number is required.
        password is required.
        checked email or mobile_number is already exist or not.
        checked user is active or not.
    If user is authenticated so we return user instance.
    """
    # CREATE FORM FOR GET CREATE SESSION DETAIL FROM FRONTEND.
    email = serializers.CharField(style={"input_type": "text"}, write_only=True, required=False, allow_blank=True)
    mobile_number = serializers.CharField(style={"input_type": "text"}, write_only=True, required=False,
                                          allow_blank=True)
    password = serializers.CharField(style={"input_type": "text"}, write_only=True)

    # CREATE A VALIDATE FUNCTION FOR LOGIN VALIDATION.
    def validate(self, data):
        email = data.get("email", "")
        mobile_number = data.get("mobile_number", "")
        password = data.get("password", "")
        user = ""
        if email:
            if User.objects.filter(email=email).filter(is_active=False).exists():
                mes = "User not activate."  # MESSAGE IF USER NOT ACTIVE.
                raise CustomValidationError(
                    mes,
                    'message',
                    status.HTTP_400_BAD_REQUEST
                )  # DISPLAY ERROR MESSAGE.
            else:
                user = cb.authenticate(self, identifier=email, password=password)
        elif mobile_number:
            if User.objects.filter(mobile_number=mobile_number).filter(is_active=False).exists():
                mes = "User not activate"  # MESSAGE IF USER NOT ACTIVE.
                raise CustomValidationError(
                    mes,
                    'message',
                    status.HTTP_400_BAD_REQUEST
                )  # DISPLAY ERROR MESSAGE.
            else:
                user = cb.authenticate(self, identifier=mobile_number, password=password)
        else:
            mes = "Please enter email or mobile number for login."  # MESSAGE IF INVALID LOGIN DETAIL.
            raise CustomValidationError(
                mes,
                'email',
                status.HTTP_400_BAD_REQUEST
            )  # DISPLAY ERROR MESSAGE.
        if user:
            if user is not None:  # CHECK LOGIN DETAIL VALID OR NOT.
                return user  # RETURN USER INSTANCE FOR LOGIN.
        else:
            return "Not Valid"


class JobSeekerProfileSerializer(serializers.ModelSerializer):
    """
    Created a serializer class for get JobSeeker's profile data. Here we use serializers.ModelSerializer.
    Here we get data from JobSeekerProfile table, and we get only some required field like:-
        gender, dob, employment_status, description, market_information_notification, job_notification.
    """

    class Meta:
        model = JobSeekerProfile
        fields = (
            'gender',
            'dob',
            'employment_status',
            'description',
            'market_information_notification',
            'job_notification'
        )


class EducationRecordSerializer(serializers.ModelSerializer):
    """
    Created a serializer class for get education record data. Here we use serializers.ModelSerializer.
    Here we get data from EducationRecord table, and we get only some required field like:-
        id, title, start_date, end_date, present, organization, description.
    """

    class Meta:
        model = EducationRecord
        fields = (
            'id',
            'title',
            'start_date',
            'end_date',
            'present',
            'organization',
            'description'
        )


class EmploymentRecordSerializer(serializers.ModelSerializer):
    """
    Created a serializer class for get employment record data. Here we use serializers.ModelSerializer.
    Here we get data from EmploymentRecord table, and we get only some required field like:-
        id, title, start_date, end_date, present, organization, description.
    """

    class Meta:
        model = EmploymentRecord
        fields = (
            'id',
            'title',
            'start_date',
            'end_date',
            'present',
            'organization',
            'description'
        )


class ResumeSerializer(serializers.ModelSerializer):
    """
    Created a serializer class for get resume data. Here we use serializers.ModelSerializer.
    Here we get data from Resume table, and we get only some required field like:-
        id, title, file_path, created_at.
    """

    class Meta:
        model = Resume
        fields = (
            'id',
            'title',
            'file_path',
            'created_at'
        )


class JobSeekerLanguageProficiencySerializer(serializers.ModelSerializer):
    """
    Created a serializer class for get JobSeeker language proficiency data. Here we use serializers.ModelSerializer.
    Here we get data from JobSeekerLanguageProficiency table, and we get only some required field like:-
        id, language, written, spoken.
    """

    class Meta:
        model = Resume
        fields = (
            'id',
            'language',
            'written',
            'spoken'
        )


class JobSeekerSkillSerializer(serializers.ModelSerializer):
    """
    Created a serializer class for get JobSeeker skills data. Here we use serializers.ModelSerializer.
    Here we get data from JobSeekerSkill table, and we get only some required field like:-
        id, skill.
    """

    class Meta:
        model = JobSeekerSkill
        fields = (
            'id',
            'skill'
        )


class JobSeekerDetailSerializers(serializers.ModelSerializer):
    """
    Created a serializer class for get Job Seeker detail. Here we use serializers.ModelSerializer.
    Here we need data form other serializers like:-
        JobSeekerProfileSerializer
        EducationRecordSerializer
        EmploymentRecordSerializer
        ResumeSerializer
        JobSeekerLanguageProficiencySerializer
        JobSeekerSkillSerializer,
            so we create function and call data from these serializer classes.

    Here we get data from user table, and we get only some required field from user table like:-
        id, email, mobile_number, country_code, display_name, image, role.
    """
    profile = serializers.SerializerMethodField()
    education_record = serializers.SerializerMethodField()
    work_experience = serializers.SerializerMethodField()
    resume = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()
    skills = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'mobile_number', 'country_code', 'display_name', 'image', 'role', 'profile',
                  'education_record', 'work_experience', 'resume', 'languages', 'skills']

    def get_profile(self, obj):
        context = dict()
        user_data = JobSeekerProfile.objects.filter(user=obj)
        get_data = JobSeekerProfileSerializer(user_data, many=True)
        if get_data.data:
            context = get_data.data[0]
        return context

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
    Created a serializer class for get employer's profile data. Here we use serializers.ModelSerializer.
    Here we get data from EmployerProfile table, and we get only some required field like:-
        organization_name, description, organization_type, license_id, license_id_file.
    """

    class Meta:
        model = EmployerProfile
        fields = (
            'description',
            'organization_type',
            'license_id',
            'license_id_file'
        )


class EmployerDetailSerializers(serializers.ModelSerializer):
    """
    Created a serializer class for get employer detail. Here we use serializers.ModelSerializer.
    Here we need data form other serializers like:-
        EmployerProfileSerializer,
            so we create function and call data from these serializer classes.

    Here we get data from user table, and we get only some required field from user table like:-
        id, email, mobile_number, country_code, display_name, image, role.
    """
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'mobile_number', 'country_code', 'display_name', 'image', 'role', 'profile']

    def get_profile(self, obj):
        context = dict()
        user_data = EmployerProfile.objects.filter(user=obj)
        get_data = EmployerProfileSerializer(user_data, many=True)
        if get_data.data:
            context = get_data.data[0]
        return context

