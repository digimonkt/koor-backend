# IMPORT PYTHON PACKAGE.
import jwt

from django.contrib.auth import login

from rest_framework import generics, response, status, permissions
from rest_framework_simplejwt.tokens import RefreshToken

# IMPORT SOME IMPORTANT FUNCTION AND DATA
from KOOR.settings import DJANGO_CONFIGURATION

# IMPORT SOME MODEL CLASS FORM SOME APP'S MODELS.PY FILE.
from .models import User, UserSession

# IMPORT SOME SERIALIZERS CLASS FROM SOME APP'S SERIALIZER.PY FILE.
from .serializer import (
    CreateUserSerializers, CreateSessionSerializers, JobSeekerDetailSerializers, EmployerDetailSerializers
)


# CREATE CLASS FOR USER REGISTRATION.
class CreateUserView(generics.GenericAPIView):
    """
    Created a class for user registration and get user detail.
    For user registration:-
        For user registration we call post method and using a serializer function CreateUserSerializers. This Class is
        permitted to any user.
            If registration is successfully complete, we send AccessToken and RefreshToken in response header with
            status code 201.
            If the user could not register, so we send an error message with a 400 status code.

    For get user detail:-
        For get user detail we call get method. This Class is permitted to only authenticated user.
        Here we use JobSeekerDetailSerializers for get job-seeker's pofile data, and we use EmployerDetailSerializers
        for get employer's profile data.
            If you get user detail successfully then we send user's serialized data with status code 200.
            If we get any error, so we send an error message with a 400 status code.
    """
    serializer_class = CreateUserSerializers  # CALL SERIALIZERS FOR REGISTRATION.
    permission_classes = [permissions.AllowAny]  # SET PERMISSION FOR ALL USER.

    def get(self, request):
        context = dict()  # CREATE A BLANK DICTIONARY AS CONTEXT.
        if self.request.user.is_authenticated:
            context = dict()
            user_id = request.GET.get('userId', None)
            try:
                if not user_id:
                    access_token = request.headers['Authorization'].replace('Bearer ', '')
                    decoded = jwt.decode(access_token, DJANGO_CONFIGURATION.SECRET_KEY, algorithms=['HS256'])
                    user_id = decoded.get('user_id')
                user_data = User.objects.filter(id=user_id)
                if user_data[0].role == "job_seeker":
                    get_data = JobSeekerDetailSerializers(user_data, many=True)
                    context["data"] = get_data.data
                elif user_data[0].role == "employer":
                    get_data = EmployerDetailSerializers(user_data, many=True)
                    context["data"] = get_data.data
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                context["error"] = str(e)
                return response.Response(
                    data=context,
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            context["detail"] = "Authentication credentials were not provided."
            return response.Response(
                data=context,
                status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        context = dict()  # CREATE A BLANK DICTIONARY AS CONTEXT.
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():  # CHECK FOR THE VALIDATION OF SERIALIZER.
            try:
                user = User.objects.get(id=serializer.validated_data.id)
                token = RefreshToken.for_user(user)  # GENERATING REFRESH TOKEN FOR THE USER.
                context["message"] = "User Created Successfully"  # MESSAGE AFTER CREATE USER.
                return response.Response(
                    data=context,
                    headers={"x-access": token.access_token, "x-refresh": token},
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                context["error"] = str(e)
                return response.Response(
                    data=context,
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:  # RETURN ERROR MESSAGE IF SERIALIZER NOT VALID.
            for field_name, field_errors in serializer.errors.items():
                context[field_name] = field_errors[0]
            return response.Response(
                data=context,
                status=status.HTTP_400_BAD_REQUEST
            )


# CREATE CLASS FOR USER LOGIN.
class CreateSessionView(generics.GenericAPIView):
    """
    Created a class for user login using a serializer function CreateSessionSerializers. This Class is
    permitted to any user.
        For User Login, we use the post method.
            If login is successfully complete, we send AccessToken and RefreshToken in response header with
            status code 200.
            If the user could not log in, so we send an error message with a 400 status code.
    """
    serializer_class = CreateSessionSerializers  # CALL SERIALIZERS FOR REGISTRATION.
    permission_classes = [permissions.AllowAny]  # SET PERMISSION FOR ALL USER.

    def post(self, request):
        context = dict()  # CREATE A BLANK DICTIONARY AS CONTEXT.
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():  # CHECK FOR THE VALIDATION OF SERIALIZER.

            try:
                if serializer.validated_data == "Not Valid":  # FUNCTION IF SERIALIZER IS NOT VALID.
                    context = dict()  # CREATE A BLANK DICTIONARY AS CONTEXT.
                    context["message"] = "Invalid Email or Mobile Number or Password"  # MESSAGE AFTER CREATE USER.
                    return response.Response(
                        data=context,
                        status=status.HTTP_401_UNAUTHORIZED
                    )
                else:
                    login(
                        request=request, user=serializer.validated_data, backend='users.backends.MobileOrEmailBackend'
                    )  # LOGIN FUNCTION FOR USER.
                    token = RefreshToken.for_user(serializer.validated_data)  # GENERATING REFRESH TOKEN FOR THE USER.
                    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                    if x_forwarded_for:
                        IPAddr = x_forwarded_for.split(',')[0]
                    else:
                        IPAddr = request.META.get('REMOTE_ADDR')
                    agent = {'User-Agent': request.headers.get('User-Agent')}
                    #  MANAGE USER SESSION DATA IN DATABASE AFTER LOGGING USER.
                    UserSession(user=serializer.validated_data, ip_address=IPAddr, agent=agent).save()
                    context["message"] = "User LoggedIn Successfully"  # MESSAGE AFTER USER LOGGING.
                    return response.Response(
                        data=context,
                        headers={"x-access": token.access_token, "x-refresh": token},
                        status=status.HTTP_201_CREATED
                    )
            except Exception as e:
                context["error"] = str(e)
                return response.Response(
                    data=context,
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:  # RETURN ERROR MESSAGE IF SERIALIZER NOT VALID.
            for field_name, field_errors in serializer.errors.items():
                context[field_name] = field_errors[0]
            return response.Response(
                data=context,
                status=status.HTTP_400_BAD_REQUEST
            )
