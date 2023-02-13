from django.shortcuts import get_object_or_404

from rest_framework import (
    generics, response, status, permissions, serializers
)

from user_profile.models import EmployerProfile

from .serializers import (
    UpdateAboutSerializers,
    CreateJobsSerializers
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


class CreateJobsView(generics.CreateAPIView):
    """
    CreateJobsView - A view to handle the creation of jobs.

    This class inherits from generics.CreateAPIView and is responsible for creating jobs in the system. It uses the
    CreateJobsSerializers serializer to validate and save the job data. Only authenticated users with the role of
    "employer" are allowed to create jobs.

    If the job data is valid and the user is authorized, a 201 status code with a success message is returned. If
    there is a validation error, a 400 status code with the validation error message is returned. If there is any
    other exception, a 400 status code with the exception message is returned.

    Attributes:
        serializer_class (CreateJobsSerializers): The serializer class responsible for validating and saving the job
        data.
        permission_classes (list): A list of permission classes with only permissions.IsAuthenticated to ensure that
        only authenticated users can create jobs.
    """
    serializer_class = CreateJobsSerializers
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        context = dict()
        serializer = self.serializer_class(data=request.data)
        try:
            if self.request.user.role == "employer":
                serializer.is_valid(raise_exception=True)
                serializer.save(self.request.user)
                context["message"] = "Job added successfully."
                return response.Response(
                    data=context,
                    status=status.HTTP_201_CREATED
                )
            else:
                context['message'] = "You are not authorized for create job."
                return response.Response(
                    data=context,
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except serializers.ValidationError:
            return response.Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print(e)
            return response.Response(
                
                data=str(e),
                status=status.HTTP_400_BAD_REQUEST
            )
