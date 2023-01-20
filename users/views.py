# IMPORT PYTHON PACKAGE.
from rest_framework import generics, response, status, permissions
from rest_framework_simplejwt.tokens import RefreshToken

# IMPORT SOME MODEL CLASS FORM SOME APP'S MODELS.PY FILE.
from .models import User

# IMPORT SOME SERIALIZERS CLASS FROM SOME APP'S SERIALIZER.PY FILE.
from .serializer import (
    UserRegistrationSerializers
)


# CREATE CLASS FOR USER REGISTRATION.
class UserRegistrationView(generics.GenericAPIView):
    """
    Created a class for user registration using a serializer function UserRegistrationSerializers. This Class is
    permitted to any user.
        For User Registration, we use the post method.
            If registration is successfully complete, we send AccessToken and RefreshToken in response header with
            status code 201.
            If the user could not register, so we send an error message with a 400 status code.
    """
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

