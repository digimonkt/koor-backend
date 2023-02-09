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
    View class for creating job details.

    This view class is based on the `generics.CreateAPIView` class and extends its functionality to handle the creation
    of job details objects. The view requires authentication and only allows users with the "employer" role to create
    job details. The view uses the `CreateJobsSerializers` serializer class to validate and save the job details.

    In case of a successful creation, the view returns a response with a status code of `HTTP_201_CREATED` and a
    message indicating that the job was added successfully.

    In case of validation errors, the view returns a response with a status code of `HTTP_400_BAD_REQUEST` and a message
    indicating the validation errors.

    In case of unauthorized access, the view returns a response with a status code of `HTTP_401_UNAUTHORIZED` and a
    message indicating that the user is not authorized to create a job.

    In case of any other exceptions, the view returns a response with a status code of `HTTP_400_BAD_REQUEST` and a
    message indicating the exception that occurred.
    """

    serializer_class = CreateJobsSerializers
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        context = dict()
        serializer = self.serializer_class(data=request.data)
        try:
            if self.request.user.role == "employer":
                serializer.is_valid(raise_exception=True)
                serializer.save(user=self.request.user)
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
            return response.Response(
                data=str(e),
                status=status.HTTP_400_BAD_REQUEST
            )
