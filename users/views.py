from django.contrib.auth import login
from rest_framework import generics
from rest_framework import response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import (
    UserRegistrationSerializers, UserLoginSerializers
)
from .models import User


# CREATE CLASS FOR USER REGISTRATION.
class UserRegistrationView(generics.GenericAPIView):
    serializer_class = UserRegistrationSerializers  # CALL SERIALIZERS FOR REGISTRATION.
    permission_classes = [AllowAny]  # SET PERMISSION FOR ALL USER.

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
                context["error"] = e
                return response.Response(data=context)
        else:
            return response.Response(serializer.errors)  # RETURN ERROR MESSAGE IF SERIALIZER NOT VALID.


# CREATE CLASS FOR USER LOGIN.
class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializers  # CALL SERIALIZERS FOR REGISTRATION.
    permission_classes = [AllowAny]  # SET PERMISSION FOR ALL USER.

    def post(self, request):
        context = dict()  # CREATE A BLANK DICTIONARY AS CONTEXT.
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():  # CHECK FOR THE VALIDATION OF SERIALIZER.

            try:
                if serializer.validated_data == "Not Valid":
                    context = dict()  # CREATE A BLANK DICTIONARY AS CONTEXT.
                    context["message"] = "Invalid Email or Mobile Number or Password"  # MESSAGE AFTER CREATE USER.
                    return response.Response(data=context, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    login(request, serializer.validated_data)  # LOGIN FUNCTION.
                    user = User.objects.get(id=serializer.validated_data.id)
                    token = RefreshToken.for_user(user)  # GENERATING REFRESH TOKEN FOR THE USER.
                    context["message"] = "User LoggedIn Successfully"  # MESSAGE AFTER CREATE USER.
                    return response.Response(data=context, headers={"x-access": token.access_token, "x-refresh": token},
                                             status=status.HTTP_201_CREATED)
            except Exception as e:
                context["error"] = e
                return response.Response(data=context)
        else:
            return response.Response(serializer.errors)  # RETURN ERROR MESSAGE IF SERIALIZER NOT VALID.
