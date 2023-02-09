from django.shortcuts import get_object_or_404

from rest_framework import (
    generics, response, status, permissions, serializers
)

from user_profile.models import EmployerProfile

from .serializers import (
    UpdateAboutSerializers
)


class UpdateAboutView(generics.GenericAPIView):
    """
    A class-based view for updating the 'about' information of an EmployerProfile.

    This view is designed to handle PATCH requests and is only accessible by authenticated users. 
    The view uses the `UpdateAboutSerializers` class as the serializer for handling the incoming data and 
    performing validation. 

    If the request data is valid, the view updates the `EmployerProfile` instance associated with the current user 
    and returns a success message. If the request data is not valid, the view returns an error message.

    Attributes:
        - serializer_class (UpdateAboutSerializers): The serializer class for handling incoming data.
        - permission_classes (list): The permission classes required for accessing this view, where only authenticated 
                                      users are allowed.
    """
    
    serializer_class = UpdateAboutSerializers
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        context = dict()
        profile_instance = get_object_or_404(EmployerProfile, user=request.user)
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
