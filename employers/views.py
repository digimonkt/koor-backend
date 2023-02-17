from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework import (
    generics, response, status, 
    permissions, serializers, filters
)

from core.pagination import CustomPagination

from users.models import User

from user_profile.models import EmployerProfile

from jobs.models import JobDetails

from jobs.serializers import GetJobsSerializers

from .serializers import (
    UpdateAboutSerializers,
    CreateJobsSerializers,
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


class JobsView(generics.ListAPIView):
    """
    A view class that returns a list of JobDetails instances.

    Attributes:
            - `serializer_class`: A serializer class used to serialize the JobDetails instances.
            - `permission_classes`: A list of permission classes that a user must pass in order to access the view.
            - `queryset`: A QuerySet instance representing the list of JobDetails instances. The queryset is not
                defined in the class, but it can be defined in the get_queryset method or set dynamically in the
                dispatch method.
            - `filter_backends`: A list of filter backend classes used to filter the queryset.
            - `search_fields`: A list of fields on which the search filtering is applied.
            - `pagination_class`: A pagination class that is used to paginate the result set.

    """
    serializer_class = GetJobsSerializers
    permission_classes = [permissions.IsAuthenticated]
    queryset = None
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    pagination_class = CustomPagination

    def post(self, request):
        """
        Create a new job post for an employer.

        Args:
            - `request`: HTTP request object containing the job post data.

        Returns:
            - HTTP response object with a success or error message and status code.

        Raises:
            - `ValidationError`: If the job post data is invalid.
            - `Exception`: If there is an unexpected error during job post creation.
        """
        context = dict()
        serializer = CreateJobsSerializers(data=request.data)
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
            return response.Response(
                data=str(e),
                status=status.HTTP_400_BAD_REQUEST
            )
            
    def get_queryset(self, **kwargs):
        """
        A method that returns a queryset of `JobDetails instances`. It filters the queryset based on the `employer ID`
        provided in the `request query parameters`.
        If the `'employerId'` parameter is provided, it filters the queryset to include only the JobDetails instances
        associated with the specified `user ID`. Otherwise, it returns `all JobDetails` instances.

        Args:
            **kwargs: A dictionary of keyword arguments.

        Returns:
            QuerySet: A filtered queryset of JobDetails instances.

        """  
        user_id = self.request.GET.get('employerId', None)
        if not user_id:
            user_id = self.request.user.id
        user_data = User.objects.get(id=user_id)
        return JobDetails.objects.filter(user=user_data).order_by('-created')