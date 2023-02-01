# IMPORT PYTHON PACKAGE.
import jwt

from django.contrib.auth import login
from django.shortcuts import get_object_or_404

from rest_framework import generics, response, status, permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

# IMPORT SOME IMPORTANT FUNCTION AND DATA
from KOOR.settings import DJANGO_CONFIGURATION
from core.utils import get_user_instance
from user_profile.models import EmployerProfile

# IMPORT SOME MODEL CLASS FORM SOME APP'S MODELS.PY FILE.
from users.models import User, UserSession

# IMPORT SOME SERIALIZERS CLASS FROM SOME APP'S SERIALIZER.PY FILE.
from .serializer import (
    UpdateEmployerAboutSerializers
)


# CREATE CLASS FOR USER REGISTRATION.
class UpdateEmployerAboutView(generics.GenericAPIView):
    """
    Created a class for update employer about and update employer detail.
    For user profile update:-
        For update employer profile data we call patch method and using a serializer function
        UpdateEmployerAboutSerializers. This Class is permitted only for authenticated user. We use multipart/form-data
        for upload file.
            If profile update successfully, we send a response message with status code 201.
            If the profile not update, so we send an error message with a 400 status code.

    """
    serializer_class = UpdateEmployerAboutSerializers
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        context = dict()
        user_instance = get_user_instance(request)
        if EmployerProfile.objects.filter(user=user_instance).exists():
            profile_instance = get_object_or_404(EmployerProfile, user=user_instance)
        else:
            EmployerProfile(user=user_instance).save()
            profile_instance = get_object_or_404(EmployerProfile, user=user_instance)

        serializer = self.serializer_class(data=request.data, instance=profile_instance, partial=True)
        if serializer.is_valid():
            try:
                if serializer.update(profile_instance, serializer.validated_data):
                    context['message'] = "Updated Successfully"
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
            for field_name, field_errors in serializer.errors.items():
                context[field_name] = field_errors[0]
            return response.Response(
                data=context,
                status=status.HTTP_400_BAD_REQUEST
            )
