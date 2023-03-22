import json, jwt
import requests
from datetime import datetime


from rest_framework import (
    status, generics, serializers,
    response, permissions
)

from random import randint

from koor.config.common import Common

from core.middleware import JWTMiddleware
from core.tokens import (
    SessionTokenObtainPairSerializer, 
    PasswordResetTokenObtainPairSerializer,
    PasswordChangeTokenObtainPairSerializer)
from core.emails import get_email_object

from user_profile.models import (
    JobSeekerProfile,
    EmployerProfile
)

from superadmin.models import GooglePlaceApi

from .models import UserSession, User
from .serializers import (
    CreateUserSerializers,
    CreateSessionSerializers,
    JobSeekerDetailSerializers,
    EmployerDetailSerializers,
    UpdateImageSerializers,
    SocialLoginSerializers
)


def unique_otp_generator():
    otp = randint(1000, 9999)
    try:
        if User.objects.get(otp=otp):
            return unique_otp_generator()
    except User.DoesNotExist:
        return otp


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
    user.last_login = datetime.now()
    user.save()
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
        response_context = dict()
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user = User.objects.get(id=serializer.data['id'])
            user.set_password(serializer.data['password'])
            user.save()
            # --------------------------------------------------------
            if user.email:
                otp = unique_otp_generator()
                full_url = self.request.build_absolute_uri()
                path = self.request.path
                Base_url = full_url.replace(path, "")
                if "?" in Base_url:
                    Base_url = Base_url.split("?")[0]
                context["yourname"] = user.email
                context["otp"] = otp
                get_email_object(
                    subject=f'OTP for Verification',
                    email_template_name='email-templates/send-forget-password-otp.html',
                    context=context,
                    to_email=[user.email, ],
                    base_url=Base_url
                )
                user.otp = otp
                user.otp_created_at = datetime.now()
                user.is_verified = True
                user.save()
                otp_token = PasswordResetTokenObtainPairSerializer.get_token(
                    user=user,
                    user_id=user.id
                )
                response_context['token'] = str(otp_token) 
            else:
                user.is_verified = True
                user.save()
            # --------------------------------------------------------
            if user.role == "job_seeker":
                JobSeekerProfile.objects.create(user=user)
            elif user.role == "employer":
                EmployerProfile.objects.create(user=user)
            user_session = create_user_session(request, user)
            token = SessionTokenObtainPairSerializer.get_token(
                user=user,
                session_id=user_session.id
            )
            response_context["message"] = "User Created Successfully"
            return response.Response(
                data=response_context,
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
            user_id = request.GET.get('userId', None)
            try:
                if not user_id:
                    user_id = request.user.id
                user_data = User.objects.get(id=user_id)
                if user_data.role == "job_seeker":

                    get_data = JobSeekerDetailSerializers(user_data)
                    context = get_data.data

                elif user_data.role == "employer":
                    get_data = EmployerDetailSerializers(user_data)
                    context = get_data.data

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


class DeleteSessionView(generics.GenericAPIView):
    """
    DeleteSessionView:
        A generic API view that handles the deletion of user sessions.

    Attributes:
        - permission_classes (List): A list of permission classes that control access to this view.

    Methods:
        - delete(self, request): Handles the deletion of user sessions based on the provided 'x-refresh' header. If the
          header is invalid or expired, an error message will be returned in the response. If the session is successfully
          deleted, a success message will be returned.

    Returns:
        - response.Response: A response object containing either an error message or a success message.
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        context = dict()
        try:
            refresh_token = request.headers.get('x-refresh')
            payload = JWTMiddleware.decode_token(refresh_token)
            UserSession.objects.filter(id=payload.get('session_id')).update(expire_at=datetime.now())
            context["message"] = "Logged Out successfully"
            return response.Response(data=context, status=status.HTTP_200_OK)
        except Exception as e:
            context["error"] = str(e)
            return response.Response(data=context, status=status.HTTP_400_BAD_REQUEST)


class DisplayImageView(generics.GenericAPIView):
    """
    API view class for displaying and updating a user's profile image.

    Attributes:
        - `serializer_class (UpdateImageSerializers)`: The serializer class used for updating the user's profile image.
        - `permission_classes (list)`: A list of permission classes that the user must have to access this view.
    """
    serializer_class = UpdateImageSerializers
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        """
        Updates the user's profile image and returns the new `image URL`.

        Args:
            - `request (HttpRequest)`: The HTTP request object.

        Returns:
            - `Response`: A JSON response containing the new image URL, or a list of errors if the request was invalid.

        Raises:
            - `HTTPError`: If the user is not authenticated.
        """
        context = dict()
        serializer = self.serializer_class(data=request.data, instance=request.user, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            if serializer.update(request.user, serializer.validated_data):
                context["image"] = str(request.user.image.file_path.url)
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
        except serializers.ValidationError:
            return response.Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class SendOtpView(generics.GenericAPIView):
    """
    A view for sending an `OTP to a user's email` address for `password recovery`.

    `Permissions`:
        - `AllowAny`: Anyone can access this view.

    `Methods`:
        - `get`: Sends an email message containing an OTP to the user's email address.

    `Returns`:
        - `Response`: A Response object with the data and HTTP status code.

    `Raises`:
        - `Exception`: If an exception occurs during the sending of the email message.

    """

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """
        Sends an email message containing an OTP to the user's email address.

        `Args`:
            - `request (HttpRequest)`: The request object.

        `Returns`:
            - `Response`: A Response object with the data and HTTP status code.

        `Raises`:
            - `Exception`: If an exception occurs during the sending of the email message.

        """

        context = dict()
        response_context = dict()
        try:
            otp = unique_otp_generator()
            full_url = self.request.build_absolute_uri()
            path = self.request.path
            Base_url = full_url.replace(path, "")
            if "?" in Base_url:
                Base_url = Base_url.split("?")[0]
            user_email = request.GET.get('email', None)
            try:
                user_instance = User.objects.get(email__iexact=user_email)
                context["yourname"] = user_email
                context["otp"] = otp
                get_email_object(
                    subject=f'OTP for Verification',
                    email_template_name='email-templates/send-forget-password-otp.html',
                    context=context,
                    to_email=[user_email, ],
                    base_url=Base_url
                )
                user_instance.otp = otp
                user_instance.otp_created_at = datetime.now()
                user_instance.save()
                token = PasswordResetTokenObtainPairSerializer.get_token(
                    user=user_instance,
                    user_id=user_instance.id
                )
                response_context['token'] = str(token.access_token)
                response_context['message'] = "OTP sent to " + user_email
                return response.Response(
                    data=response_context,
                    status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                return response.Response(
                    data={"email": "Does Not Exist"},
                    status=status.HTTP_404_NOT_FOUND
                )

        except Exception as e:
            context["error"] = str(e)
            return response.Response(
                data=context,
                status=status.HTTP_400_BAD_REQUEST
            )


class OtpVerificationView(generics.GenericAPIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request, otp):

        context = dict()
        try:
            token = self.request.GET.get('token', None)
            user_id = None
            token = jwt.decode(token, key=Common.SECRET_KEY, algorithms=Common.SIMPLE_JWT.get('ALGORITHM', ['HS256', ]))
            if 'user_id' in token:
                user_id = token['user_id']
            user_instance = User.objects.get(otp=otp, id=user_id)
            token = PasswordChangeTokenObtainPairSerializer.get_token(
                    user=user_instance,
                    user_id=user_instance.id,
                    otp=user_instance.otp
                )
            context['token'] = str(token.access_token)
            return response.Response(
                data=context,
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return response.Response(
                data={"otp": "Invalid OTP or Token"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["error"] = str(e)
            return response.Response(
                data=context,
                status=status.HTTP_400_BAD_REQUEST
            )


class ChangePasswordView(generics.GenericAPIView):
    """
    A view to change a user's password using an OTP.

    - Methods:
        - put(self, request):
            Changes the password of a user identified by their OTP.

    - Attributes:
        - permission_classes : list
            A list of permission classes that allow any user to access this view.
    """
    permission_classes = [permissions.AllowAny]

    def put(self, request):
        """
        Changes the password of a user identified by their `OTP`.

        - `Parameters`:
            - `request` : HttpRequest
                The HTTP request object.

        - `Returns:
            - A JSON response containing the status of the password change operation.
            - If the operation was successful, the response has a 200 OK status code.
            - If the OTP does not exist, the response has a 404 NOT FOUND status code.
            - If there was an error, the response has a 400 BAD REQUEST status code.
        """

        context = dict()
        try:
            password = request.data['password']
            token = self.request.GET.get('token', None)
            user_id = None
            token = jwt.decode(token, key=Common.SECRET_KEY, algorithms=Common.SIMPLE_JWT.get('ALGORITHM', ['HS256', ]))
            if 'user_id' in token:
                user_id = token['user_id']
                otp = token['otp']
            user_instance = User.objects.get(otp=otp, id=user_id)
            user_instance.otp = None
            user_instance.otp_created_at = None
            user_instance.set_password(password)
            user_instance.is_verified = True
            user_instance.save()
            context['message'] = "Password updated successfully."
            return response.Response(
                data=context,
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return response.Response(
                data={"otp": "Invalid token"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["error"] = str(e)
            return response.Response(
                data=context,
                status=status.HTTP_400_BAD_REQUEST
            )


class GetLocationView(generics.GenericAPIView):
    """
    View that retrieves the Google Places APIs autocomplete suggestions based on a provided search location.

    GET Parameters:
        - `search`: A string representing the search location.

    Returns:
        Returns a Response object with a JSON-formatted dictionary of autocomplete suggestions and a status code of
        200 (OK).
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """
        Retrieves the Google Places APIs autocomplete suggestions based on a provided search location.

        Returns:
            Returns a Response object with a JSON-formatted dictionary of autocomplete suggestions and a status code of
            200 (OK).
        """
        context = dict()
        search_location = self.request.GET.get('search', None)
        try:
            api_data = GooglePlaceApi.objects.filter(status=True).last()
            api_key = api_data.api_key
            api_response = requests.get(
                'https://maps.googleapis.com/maps/api/place/autocomplete/json?input={0}&key={1}'.format(
                    search_location, api_key
                )
            )
            api_response_dict = api_response.json()
            return response.Response(
                data=api_response_dict,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            context["error"] = str(e)
            return response.Response(
                data=context,
                status=status.HTTP_400_BAD_REQUEST
            )


class SocialLoginView(generics.GenericAPIView):
    """
    SocialLoginView is a view class that handles social login for users.

    The class contains a `post` method that accepts a `request` object and validates the data using the
    `SocialLoginSerializers` serializer class. It then checks if the user with the given email already exists,
    and if not, it creates a new user with the validated data. It also checks if the role of the user matches the role
    provided in the request data. If the user is successfully authenticated, it creates a user session and generates an
    access token and a refresh token. Finally, it returns a response with a success message, access token, and refresh
    token.

    Parameters:
        - `generics.GenericAPIView`: A generic class-based view that handles HTTP requests.

    Returns:
        - `response.Response`: A response object that contains a success message, access token, and refresh token.

    Raises:
        - `serializers.ValidationError`: If the serializer data is invalid, it raises a `serializers.ValidationError`.
    """

    serializer_class = SocialLoginSerializers
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        context = dict()
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            if User.objects.filter(email=serializer.validated_data['email']).exists():
                user = User.objects.get(email=serializer.validated_data['email'])
            else:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                user = User.objects.get(id=serializer.data['id'])
                if user.role == "job_seeker":
                    JobSeekerProfile.objects.create(user=user)
                elif user.role == "employer":
                    EmployerProfile.objects.create(user=user)
            if user.role != serializer.validated_data['role']:
                context["message"] = "Email registered with wrong role."
                return response.Response(
                    data=context,
                    headers={"x-access": token.access_token, "x-refresh": token},
                    status=status.HTTP_404_NOT_FOUND
                )
            user_session = create_user_session(request, user)
            token = SessionTokenObtainPairSerializer.get_token(
                user=user,
                session_id=user_session.id
            )
            context["message"] = "User Login Successfully"
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


class VerificationView(generics.GenericAPIView):
    """
    A class-based view that handles the verification of user's OTP and sets the user's verification status to True.
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, otp):
        """
        Handle GET requests for the view.

        Args:
            - `request`: The HTTP request object.
            - `otp`: The OTP received by the user for verification.

        Returns:
            - A Response object with status code 200 if the user is successfully verified.
            - A Response object with status code 404 if the user's OTP or token is invalid.
            - A Response object with status code 400 if there is any other error during the verification process.
        """

        context = dict()
        try:
            token = self.request.GET.get('token', None)
            user_id = None
            token = jwt.decode(token, key=Common.SECRET_KEY, algorithms=Common.SIMPLE_JWT.get('ALGORITHM', ['HS256', ]))
            if 'user_id' in token:
                user_id = token['user_id']
            
            user_instance = User.objects.get(otp=otp, id=user_id)
            if user_instance.is_verified == True:
                context['message'] = "Your email address already verified."
            else:
                user_instance.otp = None
                user_instance.otp_created_at = None
                user_instance.is_verified = True
                user_instance.save()
                context['message'] = "Your email address is verified."
            return response.Response(
                data=context,
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return response.Response(
                data={"otp": "Invalid OTP or Token"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["error"] = str(e)
            return response.Response(
                data=context,
                status=status.HTTP_400_BAD_REQUEST
            )
