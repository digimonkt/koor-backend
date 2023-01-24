# IMPORT PYTHON PACKAGE.
from rest_framework import exceptions
from rest_framework import serializers

# IMPORT CUSTOM AUTHENTICATE FUNCTION FORM BACKENDS.PY FILE.
from .backends import MobileOrEmailBackend as cb

# IMPORT SOME MODEL CLASS FROM SOME APP'S MODELS.PY FILE.
from .models import User


# CREATE SERIALIZER FOR USER REGISTRATION.
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
            # CHECK MOBILE NUMBER ALREADY REGISTERED OR NOT.
            if User.objects.filter(mobile_number=mobile_number).exists():
                mes = "Mobile number already exist."  # MESSAGE IF USER ALREADY REGISTERED.
                raise exceptions.APIException(mes)  # CALL MESSAGE IF USER ALREADY REGISTERED.
        if email or mobile_number:
            try:
                user_data = User(
                    email=email,
                    mobile_number=mobile_number,
                    country_code=country_code,
                    is_active=True,
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


# CREATE SERIALIZER FOR USER LOGIN.
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
    # CREATE FORM FOR GET USER DETAIL FROM FRONTEND..
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
        try:
            if email:
                if User.objects.filter(email=email).filter(is_active=False).exists():
                    mes = "User not activate."  # MESSAGE IF USER NOT ACTIVE.
                    raise exceptions.APIException(mes)  # DISPLAY ERROR MESSAGE.
                else:
                    user = cb.authenticate(self, identifier=email, password=password)
            elif mobile_number:
                if User.objects.filter(mobile_number=mobile_number).filter(is_active=False).exists():
                    mes = "User not activate"  # MESSAGE IF USER NOT ACTIVE.
                    raise exceptions.APIException(mes)  # DISPLAY ERROR MESSAGE.
                else:
                    user = cb.authenticate(self, identifier=mobile_number, password=password)
            if user:
                if user is not None:  # CHECK LOGIN DETAIL VALID OR NOT.
                    return user  # RETURN USER INSTANCE FOR LOGIN.
                else:
                    return "Not Valid"
            else:
                mes = "Please enter email or mobile number for login."  # MESSAGE IF INVALID LOGIN DETAIL.
                raise exceptions.APIException(mes)  # DISPLAY ERROR MESSAGE.
        except Exception as e:
            raise exceptions.APIException(e)  # CALL MESSAGE IF USER NOT REGISTERED.
