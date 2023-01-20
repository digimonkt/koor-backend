# IMPORT PYTHON PACKAGE.
from rest_framework import exceptions
from rest_framework import serializers


# IMPORT SOME MODEL CLASS FROM SOME APP'S MODELS.PY FILE.
from .models import User


# CREATE SERIALIZER FOR USER REGISTRATION.
class UserRegistrationSerializers(serializers.ModelSerializer):
    """
    Created a serializer class for user registration. Here we use ModelSerializer, using User model.
    Here we create some validation like:
        email or mobile_number is required.
        password is required.
        check email or mobile_number is already exist or not.
    After create user return user instance.
    """
    class Meta:
        model = User
        fields = ['email', 'mobile_number', 'password', 'profile_role', 'country_code']

    # CREATE A VALIDATION FUNCTION FOR INSERT USER RECORD INTO USER TABLE.
    def validate(self, data):
        email = data.get("email", "")
        mobile_number = data.get("mobile_number", "")
        password = data.get("password", "")
        profile_role = data.get("profile_role", "")
        country_code = data.get("country_code", "")
        if email:
            if User.objects.filter(email=email).exists():  # CHECK EMAIL ALREADY REGISTERED OR NOT.
                mes = "Email already exist."  # MESSAGE IF USER ALREADY REGISTERED.
                raise exceptions.APIException(mes)  # CALL MESSAGE IF USER ALREADY REGISTERED.
        if mobile_number:
            if User.objects.filter(mobile_number=mobile_number).exists():  # CHECK MOBILE NUMBER ALREADY REGISTERED OR NOT.
                mes = "Mobile number already exist."  # MESSAGE IF USER ALREADY REGISTERED.
                raise exceptions.APIException(mes)  # CALL MESSAGE IF USER ALREADY REGISTERED.
        if email or mobile_number:
            try:
                user_data = User(
                    email=email,
                    mobile_number=mobile_number,
                    country_code=country_code,
                    is_active=False,
                    profile_role=profile_role
                )  # SET DATA INTO USER TABLE FOR CRATE USER BUT USER NOT CREATED AT THAT MOMENT.
                user_data.set_password(password)  # SET PASSWORD FOR USER.

                user_data.save()  # SAVE USER DATA INTO TABLE.
                return user_data  # RETURN SOME INFORMATION ACCORDING TO FUNCTION.
            except Exception as e:
                raise exceptions.APIException(e)  # CALL MESSAGE IF USER NOT REGISTERED.
        else:
            # MESSAGE IF EMAIL AND MOBILE NUMBER BOTH FIELD ARE BLANK.
            mes = "Mobile number or Email is required for user registration."
            raise exceptions.APIException(mes)  # CALL MESSAGE IF USER ALREADY REGISTERED.
