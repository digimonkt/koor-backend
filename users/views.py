from django.db.models import (
    Q
)
import json, jwt
import requests
from datetime import datetime, date
from django.utils import timezone
import uuid
import hashlib
from django_filters import rest_framework as django_filters
from django.db.models import Sum

from rest_framework import (
    status, generics, serializers,
    response, permissions, filters
)

from random import randint

from koor.config.common import Common

from core.middleware import JWTMiddleware
from core.tokens import (
    SessionTokenObtainPairSerializer,
    PasswordResetTokenObtainPairSerializer,
    PasswordChangeTokenObtainPairSerializer
)

from core.emails import get_email_object
from core.pagination import CustomPagination

from user_profile.models import (
    JobSeekerProfile, EmployerProfile,
    VendorProfile, UserFilters, UserAnalytic
)

from jobs.models import JobSubCategory

from notification.models import Notification

from superadmin.models import GooglePlaceApi

from .models import (
    UserSession, User, VisitorLog
)
from .filters import UsersFilter
from .serializers import (
    CreateUserSerializers,
    CreateSessionSerializers,
    JobSeekerDetailSerializers,
    EmployerDetailSerializers,
    VendorDetailSerializers,
    UpdateImageSerializers,
    SocialLoginSerializers,
    UserFiltersSerializers,
    GetUserFiltersSerializers,
    SearchUserSerializers
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
            if user.role != "employer":
                if user.email:
                    user_email = user.email + str(datetime.now())
                    result = hashlib.md5(user_email.encode())
                    hash_url = Common.FRONTEND_BASE_URL + "/activation?verify-token=" + str(result.hexdigest())
                    user.verification_token = str(result.hexdigest())
                    user.otp_created_at = datetime.now()
                else:
                    user_mobile_number = str(user.mobile_number)
                    result = hashlib.md5(user_mobile_number.encode())
                    hash_url = Common.FRONTEND_BASE_URL + "/activation?verify-token=" + str(result.hexdigest())
                    user.verification_token = str(result.hexdigest())
                    user.otp_created_at = datetime.now()
            else:
                user.is_verified = True
                if user.role == 'admin':
                    user.is_staff = True
                    user.is_superuser = True
            # # -----------------------------------
            user.save()
            # if user.email:
            #     otp = unique_otp_generator()
            #     context["yourname"] = user.email
            #     context["otp"] = otp
            #     get_email_object(
            #         subject=f'New Registration for Koor Jobs',
            #         email_template_name='email-templates/new/new-login-detected.html',
            #         # email_template_name='email-templates/send-forget-password-otp.html',
            #         context=context,
            #         to_email=[user.email, ]
            #     )
            #     user.otp = otp
            #     user.otp_created_at = datetime.now()
            #     # user.is_verified = True
            #     user.save()
            #     otp_token = PasswordResetTokenObtainPairSerializer.get_token(
            #         user=user,
            #         user_id=user.id
            #     )
            #     response_context['token'] = str(otp_token)
            # else:
            #     # user.is_verified = True
            #     user.save()
            # !!!!!!!!!!!!!!!!!!!!!!!!!! EMAIL CODE SENT START !!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
            if user.role == "job_seeker":
                JobSeekerProfile.objects.create(user=user)
            elif user.role == "employer":
                EmployerProfile.objects.create(user=user)
            elif user.role == "vendor":
                VendorProfile.objects.create(user=user)
            user_session = create_user_session(request, user)
            token = SessionTokenObtainPairSerializer.get_token(
                user=user,
                session_id=user_session.id
            )
            response_context["message"] = "User Created Successfully"
            if user.role != 'employer' and user.email:
                if user.role == 'job_seeker':
                    context['product'] = 'job'
                elif user.role == 'vendor':
                    context['product'] = 'tender'
                context["yourname"] = user.email
                context["hash_url"] = hash_url
                get_email_object(
                    subject=f'Welcome to KOOR',
                    email_template_name='email-templates/new/activate-your-account.html',
                    context=context,
                    to_email=[user.email, ]
                )
            else:
                if user.role == 'employer':
                    context['product'] = 'job'
                    if user.email:
                        context["yourname"] = user.email
                        get_email_object(
                            subject=f'Welcome to KOOR',
                            email_template_name='email-templates/new/activate-employer-account.html',
                            context=context,
                            to_email=[user.email, ]
                        )
                admin_email = []
                admin_data = User.objects.filter(role='admin')
                for get_admin in admin_data:
                    if get_admin.email:
                        admin_email.append(get_admin.email)
                if user.email:
                    context["user_name"] = user.name
                    context["user_email"] = str(user.email)
                    if user.country_code:
                        context["user_mobile_number"] = str(user.country_code) + "-" + str(user.mobile_number)
                    get_email_object(
                        subject=f'New Employer Registration: Action Required',
                        email_template_name='email-templates/new/employer-registration.html',
                        context=context,
                        to_email=admin_email
                    )
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
        user_id = request.GET.get('userId', None)
        try:
            if not user_id:
                if request.user and request.user.is_authenticated:
                    user_id = request.user.id
                else:
                    context["detail"] = "Authentication credentials were not provided."
                    return response.Response(
                        data=context,
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            user_data = User.objects.get(id=user_id)
            session_id = UserSession.objects.filter(user=user_data).order_by('-created').first()
            if user_data.role == "job_seeker":
                get_data = JobSeekerDetailSerializers(user_data)
                context = get_data.data
            elif user_data.role == "employer":
                get_data = EmployerDetailSerializers(user_data)
                context = get_data.data
            elif user_data.role == "vendor":
                get_data = VendorDetailSerializers(user_data)
                context = get_data.data
            context['session_id'] = session_id.id if session_id else ''
            if user_data.role == "admin":
                context['email'] = user_data.email
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
            if request.user.role == "admin":
                user_id = request.GET.get('userId', None)
                if user_id:
                    user_instance = User.objects.get(id=user_id)
                    if serializer.update(user_instance, serializer.validated_data):
                        user_instance = User.objects.get(id=user_id)
                        context["image"] = str(user_instance.image.file_path.url)
                        return response.Response(
                            data=context,
                            status=status.HTTP_200_OK
                        )
                else:
                    context['message'] = "userId is required for update employer profile."
                    return response.Response(
                        data=context,
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            else:
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
            user_email = request.GET.get('email', None)
            user_role = request.GET.get('role', None)
            try:
                user_instance = User.objects.get(email__iexact=user_email)
                if user_instance.role != user_role:
                    return response.Response(
                        data={"email": "User not exist as " + str(user_role)},
                        status=status.HTTP_404_NOT_FOUND
                    )
                context["yourname"] = user_email
                context["otp"] = otp
                if user_instance.is_verified:
                    email_template_name='email-templates/new/otp-verification.html'
                else:
                    email_template_name='email-templates/new/account-verification.html'
                get_email_object(
                    subject=f'OTP for Verification',
                    email_template_name=email_template_name,
                    # email_template_name='email-templates/send-forget-password-otp.html',
                    context=context,
                    to_email=[user_email, ]
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
            # user_instance.is_verified = True
            user_instance.save()
            Notification.objects.create(
                user=user_instance, notification_type='password_update',
                created_by=user_instance
            )
            if user_instance.email:
                email_context = dict()
                if user_instance.name:
                    user_name = user_instance.name
                else:
                    user_name = user_instance.email
                email_context["yourname"] = user_name
                email_context["notification_type"] = "update password"
                email_context["job_instance"] = "update password"
                get_email_object(
                    subject=f'Notification for update password',
                    email_template_name='email-templates/send-notification-old.html',
                    context=email_context,
                    to_email=[user_instance.email, ]
                )
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
            if serializer.validated_data['source'] == 'facebook':
                if User.objects.filter(social_login_id=serializer.validated_data['social_login_id']).exists():
                    user = User.objects.get(social_login_id=serializer.validated_data['social_login_id'])
                    user.is_verified = True
                    user.save()
                else:
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    user = User.objects.get(id=serializer.data['id'])
                    if user.role == "job_seeker":
                        JobSeekerProfile.objects.create(user=user)
                    elif user.role == "employer":
                        EmployerProfile.objects.create(user=user)
                    elif user.role == "vendor":
                        VendorProfile.objects.create(user=user)
                if user.role != serializer.validated_data['role']:
                    context["message"] = ["Account already registered with another role."]
                    context["role"] = [user.role]
                    return response.Response(
                        data=context,
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
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
                    elif user.role == "vendor":
                        VendorProfile.objects.create(user=user)
                if user.role != serializer.validated_data['role']:
                    context["message"] = ["Email already registered with another role."]
                    context["role"] = [user.role]
                    return response.Response(
                        data=context,
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


class SearchView(generics.ListAPIView):
    """
    A view that returns a list of candidates filtered by role and optionally searched by title.
    The `role` parameter is required in the URL path.
    The `limit` query parameter can be used to paginate the results.

    - `Serializer class`: SearchUserSerializers
    - `Permission classes`: AllowAny
    - `Queryset`: all User objects
    - `Filter backends`: SearchFilter
    - `Search fields`: 'title'

    HTTP methods:
        - `GET`: returns a paginated list of candidates filtered by role and optionally searched by title.

    Sample URLs:
        - /candidates/developers/?limit=10&search=python
        - /candidates/managers/?search=project+management
    """

    serializer_class = SearchUserSerializers
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.filter(is_active=True)
    filter_backends = [filters.SearchFilter, django_filters.DjangoFilterBackend]
    filterset_class = UsersFilter
    search_fields = [
        'name', 'email'
    ]
    pagination_class = CustomPagination

    def list(self, request, role):
        """
        Returns a paginated list of candidates filtered by role and optionally searched by title.

        Parameters:
            - `role`: str, the role of the candidates to retrieve (e.g., 'developers', 'managers')

        Query parameters:
            - `limit`: int, the maximum number of results to return per page (default: 100)
            - `search`: str, the keyword(s) to search in the 'title' field of the candidates

        Returns:
        A JSON response with the following keys:
            - `count`: int, the total number of candidates matching the filter/search criteria
            - `next`: str or None, a URL to the next page of results (if any)
            - `previous`: str or None, a URL to the previous page of results (if any)
            - `results`: list of dicts, the serialized representations of the candidates matching the 
                filter/search criteria
        """
        emp_context = dict()
        if self.request.user:
            emp_context = {"user": self.request.user}
        if role == 'job_seeker':
            queryset = self.filter_queryset(self.get_queryset().filter(role=role).filter(job_seekers_jobpreferences_user__display_in_search=True))
        else:
            queryset = self.filter_queryset(self.get_queryset().filter(role=role))
        job_category = request.GET.getlist('jobCategory')
        job_sub_category = request.GET.getlist('jobSubCategory')
        organization_type = request.GET.getlist('organizationType')
        sector = request.GET.getlist('sector')
        tag = request.GET.getlist('tag')
        fullTime = request.GET.get('fullTime')
        partTime = request.GET.get('partTime')
        contract = request.GET.get('contract')
        job_type = None
        if fullTime:
            if job_type:
                job_type = job_type | Q(job_seekers_jobpreferences_user__is_full_time=True)
            else:
                job_type = Q(job_seekers_jobpreferences_user__is_full_time=True)
        if partTime:
            if job_type:
                job_type = job_type | Q(job_seekers_jobpreferences_user__is_part_time=True)
            else:
                job_type = Q(job_seekers_jobpreferences_user__is_part_time=True)
        if contract:
            if job_type:
                job_type = job_type | Q(job_seekers_jobpreferences_user__has_contract=True)
            else:
                job_type = Q(job_seekers_jobpreferences_user__has_contract=True)
        if job_type:
            queryset = queryset.filter(job_type)
        if tag:
            queryset = queryset.filter(vendors_vendortag_user__tag__title__in=tag, vendors_vendortag_user__is_removed=False).distinct()
        if sector:
            queryset = queryset.filter(vendors_vendorsector_user__sector__title__in=sector, vendors_vendorsector_user__sector__is_removed=False).distinct()
        if organization_type:
            queryset = queryset.filter(user_profile_vendorprofile_users__organization_type__title__in=organization_type, user_profile_vendorprofile_users__is_removed=False).distinct()
        if job_sub_category:
            queryset = queryset.filter(job_seekers_categories_user__category__title__in=job_sub_category, job_seekers_categories_user__is_removed=False).distinct()
        else:
            if job_category:
                job_sub_category_data = JobSubCategory.objects.filter(category_id__title__in=job_category)
                job_sub_category = []
                for sub_category in job_sub_category_data:
                    job_sub_category.append(sub_category.title)
                queryset = queryset.filter(job_seekers_categories_user__category__title__in=job_sub_category, job_seekers_categories_user__is_removed=False).distinct()
        page = self.paginate_queryset(queryset)
        if role == "job_seeker":
            get_serializer = JobSeekerDetailSerializers
        elif role == "vendor":
            get_serializer = VendorDetailSerializers
        if page is not None:
            serializer = get_serializer(page, many=True, context=emp_context)
            return self.get_paginated_response(serializer.data)
        serializer = get_serializer(queryset, many=True, context=emp_context)
        return response.Response(serializer.data)


class UserFilterView(generics.GenericAPIView):
    """
    A view that allows authenticated users to filter and retrieve information about users.

    Attributes:
        - `serializer_class (UserFiltersSerializers)`: A serializer class that defines the format of the data being
            retrieved and filtered.
        - `permission_classes (list)`: A list of permission classes that determine which authenticated users have access
            to this view.
    """

    serializer_class = UserFiltersSerializers
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Handles a POST request to create a new resource with user data.

        Args:
            - `request (HttpRequest)`: The HTTP request object containing the data to create the resource.

        Returns:
            - `HttpResponse`: A response containing the serialized data of the created resource and the HTTP status
                code.

        Raises:
            - `serializers.ValidationError`: If the input data is invalid or does not meet the requirements of the
                serializer.
        """

        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return response.Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        except serializers.ValidationError:
            return response.Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request):
        """
            GET request handler for `UserFilters` objects.

            This method retrieves `UserFilters` objects associated with the requesting user, serializes them using the
            `GetUserFiltersSerializers` serializer, and returns them in the HTTP response.

            Args:
                - `request (rest_framework.request.Request)`: The HTTP request object.

            Returns:
                - `rest_framework.response.Response`: An HTTP response containing the serialized `UserFilters` objects,
                    or an error message if an exception occurs during processing.
        """

        context = dict()
        try:
            role = request.GET.get('role')
            user_filter_data = UserFilters.objects.filter(user=request.user, role=role)
            get_data = GetUserFiltersSerializers(user_filter_data, many=True)
            return response.Response(
                data=get_data.data,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            context["error"] = str(e)
            return response.Response(
                data=context,
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, filterId):
        """
        A function to delete a user filter instance for a user.

        Args:
        - `request (HttpRequest)`: An HTTP request object.
        - `filterId (int)`: An integer representing the ID of the user filter instance to be deleted.

        Returns:
        - A Response object with a JSON representation of a message indicating the result of the operation and the HTTP
            status code.

        Raises:
        - `UserFilters.DoesNotExist`: If the user filter instance with the given filterId and user does not exist.
        - `Exception`: If there is any other error during the deletion process.
        """

        context = dict()
        try:
            UserFilters.all_objects.get(id=filterId, user=request.user).delete(soft=False)
            context['message'] = "Filter Removed"
            return response.Response(
                data=context,
                status=status.HTTP_200_OK
            )
        except UserFilters.DoesNotExist:
            return response.Response(
                data={"filterId": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["message"] = e
            return response.Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, filterId):
        """
        A function to partially update a user filter instance for a user.

        Args:
        - `request (HttpRequest)`: An HTTP request object.
        - `filterId (int)`: An integer representing the ID of the user filter instance to be updated.

        Returns:
        - A Response object with a JSON representation of a message indicating the result of the operation and the HTTP
            status code.

        Raises:
        - `UserFilters.DoesNotExist`: If the user filter instance with the given filterId and user does not exist.
        - `Exception`: If there is any other error during the partial update process.
        """

        context = dict()
        try:
            filter_instance = UserFilters.all_objects.get(id=filterId, user=request.user)
            serializer = self.serializer_class(data=request.data, instance=filter_instance, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                if serializer.update(filter_instance, serializer.validated_data):
                    context['message'] = "Updated Successfully"
                    return response.Response(
                        data=context,
                        status=status.HTTP_200_OK
                    )
            except serializers.ValidationError:
                return response.Response(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        except UserFilters.DoesNotExist:
            return response.Response(
                data={"filterId": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["message"] = e
            return response.Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
            )

class VisitorLogView(generics.GenericAPIView):
    """
    View for logging visitor information.

    This view handles POST requests and logs the IP address and user agent information of the visitor. If a log entry
    with the same IP address and current date already exists, the view does not create a new log entry.

    Permissions:
        - `AllowAny`: Any user can access this view without authentication.

    HTTP Methods:
        - `POST`: Log visitor information.

    Returns:
        - `201 CREATED`: If the log entry is created successfully.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Log visitor information.

        This method creates a new log entry with the IP address and user agent information of the visitor. If a log
        entry with the same IP address and current date already exists, no new log entry is created.

        Args:
            - `request (HttpRequest)`: The HTTP request object.

        Returns:
            - `Response`: HTTP response object with status 201 CREATED.
        """
        context = dict()
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            IPAddr = x_forwarded_for.split(',')[0]
        else:
            IPAddr = request.META.get('REMOTE_ADDR')
        agent = {'User-Agent': request.headers.get('User-Agent')}
        if VisitorLog.objects.filter(ip_address=IPAddr, created_at=date.today()).exists():
            pass
        else:
            log_data = VisitorLog.objects.create(
                ip_address=IPAddr,
                agent=agent,
                created_at=date.today()
            )
            log_data.save()
        return response.Response(
            status=status.HTTP_201_CREATED
        )

class AnalyticView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Handle POST request to update user analytic count.

        Parameters:
            - request: The HTTP request object.

        Returns:
            - HTTP response indicating the result of the request.
        """
        
        context = dict()
        try:
            # Check if user_id is provided and valid
            if not request.data['user_id']:
                return response.Response(
                    data={'user_id': 'user_id cannot be empty.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                uuid.UUID(request.data['user_id'])
            except ValueError:
                return response.Response(
                    data={'user_id': 'Invalid user_id.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # Get the user instance
            user_instance = User.objects.get(id=request.data['user_id'])
            
            # Check if UserAnalytic record exists for the user and today's date
            if UserAnalytic.objects.filter(user=user_instance, date=date.today()).exists():
                # Update the count if record exists
                analytic_instance = UserAnalytic.objects.get(user=user_instance, date=date.today())
                UserAnalytic.objects.filter(user=user_instance, date=date.today()).update(count=int(analytic_instance.count) + 1)
            else:
                # Create a new UserAnalytic record if it doesn't exist
                UserAnalytic.objects.create(user=user_instance, date=date.today(), count=1)
                
            return response.Response(
                data={"message": "Count updated successfully."},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return response.Response(
                data={"user_id": "User Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except KeyError:
            return response.Response(
                data={'user_id': 'user_id is required.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def get(self, request):
        """
        Handle GET request to retrieve user analytic data by year.

        Parameters:
            - request: The HTTP request object.

        Returns:
            - HTTP response with the user analytic data grouped by month.
        """
        context = dict()
        if self.request.user.is_anonymous:
            context["message"] = "Login is required."
            return response.Response(
                data=context,
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            # Get the 'year' parameter from the request query parameters
            year = request.GET.get('year')
            
            # Get the user analytic data grouped by month for the specified year
            data_by_month = self.get_data_by_year(year, self.request.user)
            
            return response.Response(
                data=data_by_month,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            context["message"] = str(e)
            return response.Response(
                data=context,
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def get_data_by_year(self, year, user_instance):
        """
        Retrieve user analytic data grouped by month for the specified year.

        Parameters:
            - year: The year for which to retrieve the data.

        Returns:
            - Queryset containing the user analytic data grouped by month and the total count.
        """
        
        user_analytics = UserAnalytic.objects.filter(user=user_instance).filter(date__year=year).order_by('-date')
        data_by_month = user_analytics.values('date__year', 'date__month').annotate(total_count=Sum('count'))
        return data_by_month


class VisitorsView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        context = dict()
        IPAddr = request.data['ip']
        if VisitorLog.objects.filter(ip_address=IPAddr, created_at=date.today()).exists():
            pass
        else:
            log_data = VisitorLog.objects.create(
                ip_address=IPAddr,
                created_at=date.today()
            )
            log_data.save()
        return response.Response(
            status=status.HTTP_201_CREATED
        )


class AccountVerificationView(generics.GenericAPIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request, hash_code):

        context = dict()
        try:
            user_instance = User.objects.get(verification_token=hash_code)
            if user_instance.is_verified == True:
                context['message'] = "Your account already verified."
            else:
                now = timezone.now()
                time_difference = now - user_instance.otp_created_at
                if time_difference.total_seconds() > 24 * 3600:  # 24 hours in seconds
                    # ------------------------------------------
                    user_email = user_instance.email + str(datetime.now())
                    result = hashlib.md5(user_email.encode())
                    hash_url = Common.FRONTEND_BASE_URL + "/activation?verify-token=" + str(result.hexdigest())
                    user_instance.verification_token = str(result.hexdigest())
                    user_instance.otp_created_at = datetime.now()
                    user_instance.save()
                    context["yourname"] = user_instance.email
                    context["hash_url"] = hash_url
                    if user_instance.role != 'employer':
                        get_email_object(
                            subject=f'Welcome to KOOR',
                            email_template_name='email-templates/new/activate-your-account.html',
                            context=context,
                            to_email=[user_instance.email, ]
                        )
                    response_context['message'] = ["Verification link send to " + str(user_instance.email) + "."]
                    # ---------------------------------
                else:
                    user_instance.verification_token = None
                    user_instance.otp_created_at = None
                    user_instance.is_verified = True
                    user_instance.save()
                    user_session = create_user_session(request, user_instance)
                    token = SessionTokenObtainPairSerializer.get_token(
                        user=user_instance,
                        session_id=user_session.id
                    )
                    context["message"] = "Your account is verified."
                    return response.Response(
                        data=context,
                        headers={"x-access": token.access_token, "x-refresh": token},
                        status=status.HTTP_201_CREATED
                    )
            return response.Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
            )
        except User.DoesNotExist:
            return response.Response(
                data={"message": "Invalid Verification Link"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["error"] = str(e)
            return response.Response(
                data=context,
                status=status.HTTP_400_BAD_REQUEST
            )

class ResendVerificationView(generics.GenericAPIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        context = dict()
        response_context = dict()
        try:
            user_instance = User.objects.get(email=request.data['email'])
            if user_instance.is_verified == True:
                response_context['message'] = ["Your account already verified."]
            else:
                user_email = user_instance.email + str(datetime.now())
                result = hashlib.md5(user_email.encode())
                hash_url = Common.FRONTEND_BASE_URL + "/activation?verify-token=" + str(result.hexdigest())
                user_instance.verification_token = str(result.hexdigest())
                user_instance.otp_created_at = datetime.now()
                user_instance.save()
                context["yourname"] = user_instance.email
                context["hash_url"] = hash_url
                if user_instance.role != 'employer':
                    get_email_object(
                        subject=f'Welcome to KOOR',
                        email_template_name='email-templates/new/activate-your-account.html',
                        context=context,
                        to_email=[user_instance.email, ]
                    )
                response_context['message'] = ["Verification link send to " + str(user_instance.email) + "."]
            return response.Response(
                data=response_context,
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return response.Response(
                data={"message": ["Email address not registered"]},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["error"] = str(e)
            return response.Response(
                data=context,
                status=status.HTTP_400_BAD_REQUEST
            )
