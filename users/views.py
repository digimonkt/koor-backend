# IMPORT PYTHON PACKAGE.
from django.contrib.auth import login
from rest_framework import generics, response, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from KOOR.settings import DJANGO_CONFIGURATION

# IMPORT SOME MODEL CLASS FORM SOME APP'S MODELS.PY FILE.
from .models import User, UserSession
# IMPORT SOME SERIALIZERS CLASS FROM SOME APP'S SERIALIZER.PY FILE.
from .serializer import (
    UserRegistrationSerializers, UserLoginSerializers, UserDetailSerializers
)


# CREATE CLASS FOR USER REGISTRATION.
class UserRegistrationView(generics.GenericAPIView):
    serializer_class = UserRegistrationSerializers  # CALL SERIALIZERS FOR REGISTRATION.
    permission_classes = [permissions.AllowAny]  # SET PERMISSION FOR ALL USER.

    def post(self, request):
        context = dict()  # CREATE A BLANK DICTIONARY AS CONTEXT.
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():  # CHECK FOR THE VALIDATION OF SERIALIZER.
            try:
                user = User.objects.get(id=serializer.validated_data.id)
                token = RefreshToken.for_user(user)  # GENERATING REFRESH TOKEN FOR THE USER.
                context["message"] = "User Created Successfully"  # MESSAGE AFTER CREATE USER.
                return response.Response(data=context, headers={"x-access": token.access_token, "x-refresh": token},
                                         status=status.HTTP_201_CREATED)
            except Exception as e:
                context["error"] = str(e)
                return response.Response(data=context, status=status.HTTP_400_BAD_REQUEST)
        else:
            return response.Response(serializer.errors)  # RETURN ERROR MESSAGE IF SERIALIZER NOT VALID.


# CREATE CLASS FOR USER LOGIN.
class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializers  # CALL SERIALIZERS FOR REGISTRATION.
    permission_classes = [permissions.AllowAny]  # SET PERMISSION FOR ALL USER.

    def post(self, request):
        context = dict()  # CREATE A BLANK DICTIONARY AS CONTEXT.
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():  # CHECK FOR THE VALIDATION OF SERIALIZER.

            try:
                if serializer.validated_data == "Not Valid":  # FUNCTION IF SERIALIZER IS NOT VALID.
                    context = dict()  # CREATE A BLANK DICTIONARY AS CONTEXT.
                    context["message"] = "Invalid Email or Mobile Number or Password"  # MESSAGE AFTER CREATE USER.
                    return response.Response(data=context, status=status.HTTP_401_UNAUTHORIZED)
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
                    return response.Response(data=context, headers={"x-access": token.access_token, "x-refresh": token},
                                             status=status.HTTP_200_OK)
            except Exception as e:
                context["error"] = str(e)
                return response.Response(data=context, status=status.HTTP_400_BAD_REQUEST)
        else:
            return response.Response(serializer.errors)  # RETURN ERROR MESSAGE IF SERIALIZER NOT VALID.


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        context = dict()  # CREATE A BLANK DICTIONARY AS CONTEXT.
        try:
            refresh_token = request.headers['Refresh-Token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            context["message"] = "Logged Out successfully"  # MESSAGE AFTER USER LOGGING.
            return response.Response(data=context, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            context["error"] = str(e)
            print(e)
            return response.Response(data=context, status=status.HTTP_400_BAD_REQUEST)


# CREATE CLASS FOR USER REGISTRATION.
class UserDetailView(generics.GenericAPIView):
    serializer_class = UserDetailSerializers  # CALL SERIALIZERS FOR REGISTRATION.
    permission_classes = [IsAuthenticated]  # SET PERMISSION FOR ALL USER.

    def get(self, request):
        context = dict()
        user_id = request.data.get('userId', None)
        try:
            if not user_id:
                access_token = request.headers['Authorization'].replace('Bearer ', '')
                decoded = jwt.decode(access_token, DJANGO_CONFIGURATION.SECRET_KEY, algorithms=['HS256'])
                user_id = decoded.get('user_id')
            user_data = User.objects.filter(id=user_id)
            get_data = self.serializer_class(user_data, many=True)
            context["data"] = get_data.data
            return response.Response(data=context, status=status.HTTP_200_OK)
        except Exception as e:
            context["error"] = str(e)
            return response.Response(data=context, status=status.HTTP_400_BAD_REQUEST)