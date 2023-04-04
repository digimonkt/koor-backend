from django.shortcuts import get_object_or_404
from rest_framework import (
    generics, response, status,
    permissions, serializers
)

from user_profile.models import VendorProfile
from users.models import User
from .serializers import (
    UpdateAboutSerializers
)


class UpdateAboutView(generics.GenericAPIView):
    """
    A view for updating the VendorProfile of the currently authenticated User.

    Attributes:
        serializer_class: The serializer class to use for updating the VendorProfile.
        permission_classes: The permission classes required to access this view.

    Methods:
        patch: Handle PATCH requests to update the VendorProfile of the authenticated User.

    Returns:
        A Response object with a success or error message, and an appropriate status code.
    """

    serializer_class = UpdateAboutSerializers
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        context = dict()
        if self.request.user.role == "vendor":
            profile_instance = get_object_or_404(VendorProfile, user=request.user)
            serializer = self.serializer_class(data=request.data, instance=profile_instance, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                if serializer.update(profile_instance, serializer.validated_data):
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
        else:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
            )
