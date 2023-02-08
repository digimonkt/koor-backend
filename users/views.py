<<<<<<< HEAD
# IMPORT PYTHON PACKAGE.
import jwt

from django.contrib.auth import login

from rest_framework import generics, response, status, permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

# IMPORT SOME IMPORTANT FUNCTION AND DATA
from KOOR.settings import DJANGO_CONFIGURATION

# IMPORT SOME MODEL CLASS FORM SOME APP'S MODELS.PY FILE.
from .models import User, UserSession

# IMPORT SOME SERIALIZERS CLASS FROM SOME APP'S SERIALIZER.PY FILE.
from .serializer import (
    CreateUserSerializers, CreateSessionSerializers, JobSeekerDetailSerializers, EmployerDetailSerializers
=======
from rest_framework import (
    status, generics, serializers,
    response, permissions
>>>>>>> b6c4e2cff68ff6f1a5f87b6fafc46e529900c624
)

from core.tokens import SessionTokenObtainPairSerializer

from user_profile.models import (
    JobSeekerProfile,
    EmployerProfile
)

from .models import UserSession, User
from .serializers import (
    CreateUserSerializers,
    CreateSessionSerializers,
    JobSeekerDetailSerializers,
    EmployerDetailSerializers
)


def create_user_session(request, user):
    """
    `create_user_session` creates a new UserSession object for the given request. It retrieves the IP address from
    the request and stores the user agent in the agent field.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        IPAddr = x_forwarded_for.split(',')[0]
    else:
        IPAddr = request.META.get('REMOTE_ADDR')
    agent = {'User-Agent': request.headers.get('User-Agent')}
    user_session = UserSession.objects.create(
        user=user,
        ip_address=IPAddr,
        agent=agent
    )
    user_session.save()
    return user_session


class UserView(generics.GenericAPIView):
    """
    UserView is a generic class-based view that provides implementation for handling user data through APIs.

    Attributes:
        serializer_class (CreateUserSerializers): Serializer class to be used for serializing user data.
        permission_classes (List[permissions.AllowAny]): List of permission classes to be used for validating user
        access.
    """
    serializer_class = CreateUserSerializers
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Creates a new user, saves the password and creates a session for the user.
        
        Parameters:
            request (django.http.request.HttpRequest): The request object containing data for user creation.
        
        Returns:
            django.http.response.Response: HTTP response with status 201 and "User Created Successfully" message and 
            access and refresh tokens in header if user is created successfully. If user is not created due to invalid
            data, returns HTTP response with status 400 and error message.
        """
        context = dict()
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user = User.objects.get(id=serializer.data['id'])
            user.set_password(serializer.data['password'])
            user.save()
            if user.role == "job_seeker":
                JobSeekerProfile.objects.create(user=user)
            elif user.role == "employer":
                EmployerProfile.objects.create(user=user)
            user_session = create_user_session(request, user)

            token = SessionTokenObtainPairSerializer.get_token(
                user=user,
                session_id=user_session.id
            )
            context["message"] = "User Created Successfully"
            return response.Response(
                data=context,
                headers={"x-access": token.access_token, "x-refresh": token},
                status=status.HTTP_201_CREATED
            )
        except serializers.ValidationError:
            return response.Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request):
        """
        Retrieve user data based on user ID. If the user is authenticated, the user data is retrieved either by using
        the user ID provided in the GET request or the ID of the authenticated user. If the user is not authenticated,
        an error message is returned.

        Args:
            request (Request): The incoming request data.

        Returns:
            Response: The response containing the user data if authenticated and user data is found, otherwise an error
            message.

        Raises:
            Exception: If an error occurs while retrieving the user data.
        """
        context = dict()
        if request.user and request.user.is_authenticated:
            context = dict()
            user_id = request.GET.get('userId', None)
            try:
                if not user_id:
                    user_id = request.user.id
                user_data = User.objects.get(id=user_id)
                if user_data.role == "job_seeker":

                    get_data = JobSeekerDetailSerializers(user_data)
                    context["data"] = get_data.data

                elif user_data.role == "employer":
                    get_data = EmployerDetailSerializers(user_data)
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
                status=status.HTTP_401_UNAUTHORIZED
            )


class CreateSessionView(generics.GenericAPIView):
    """
    GenericAPIView for creating a session for a user.

    Uses the CreateSessionSerializers serializer class to validate and
    handle user data. 

    Attributes:
        serializer_class (CreateSessionSerializers): The serializer class to use.
        permission_classes ([permissions.AllowAny]): The permission classes.

    Methods:
        post(request): Handles the POST request to create a user session.
    """

    serializer_class = CreateSessionSerializers
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        context = dict()
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user_session = create_user_session(request, serializer.validated_data)
            token = SessionTokenObtainPairSerializer.get_token(
                user=serializer.validated_data,
                session_id=user_session.id
            )
            context["message"] = "User LoggedIn Successfully"
            return response.Response(
                data=context,
                headers={"x-access": token.access_token, "x-refresh": token},
                status=status.HTTP_201_CREATED
            )
        except serializers.ValidationError:
            return response.Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class DeleteSessionView(APIView):
    """
        Here we create a class DeleteSessionView for deleting the user's session. This Class is permitted to only
        authenticated users. For the delete session, we use the delete method.
            Here we need refreshToken in the request header, and we add this token to the token's blacklist table.

            - If the session deletes successfully completed, we send a message with status code 200.
            - If we get any error and the session not delete, we send an error message with a 400 status code.
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        context = dict()
        try:
            refresh_token = request.headers['X-Refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            context["message"] = "Logged Out successfully"
            return response.Response(data=context, status=status.HTTP_200_OK)
        except Exception as e:
            if e == "X-Refresh":
                context["error"] = "Token is invalid or expired"
            else:
                context["error"] = str(e)
            return response.Response(data=context, status=status.HTTP_400_BAD_REQUEST)
