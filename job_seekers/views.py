from django.shortcuts import get_object_or_404
from datetime import date

from rest_framework import (
    generics, response, status,
    permissions, serializers, filters
)
from rest_framework.pagination import LimitOffsetPagination

from core.pagination import CustomPagination

from user_profile.models import JobSeekerProfile

from employers.serializers import GetJobsSerializers

from jobs.models import JobDetails

from .serializers import (
    UpdateAboutSerializers, GetJobsDetailSerializers, EducationSerializers
)


class UpdateAboutView(generics.GenericAPIView):
    """
    A view for updating the JobSeekerProfile of the currently authenticated User.

    Attributes:
        serializer_class: The serializer class to use for updating the JobSeekerProfile.
        permission_classes: The permission classes required to access this view.

    Methods:
        patch: Handle PATCH requests to update the JobSeekerProfile of the authenticated User.

    Returns:
        A Response object with a success or error message, and an appropriate status code.
    """

    serializer_class = UpdateAboutSerializers
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        context = dict()
        profile_instance = get_object_or_404(JobSeekerProfile, user=request.user)
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


class JobSearchView(generics.ListAPIView):
    """
    API endpoint that lists all job details based on a search query.

    The endpoint requires authentication to access and returns a paginated list of job details sorted by their creation
    date in descending order. The list can be filtered by job title.

    Attributes:
        - `serializer_class`: The serializer class used to serialize job details data.
        - `permission_classes`: A list of permission classes that apply to the view.
        - `queryset`: The queryset of job details used to retrieve data.
        - `filter_backends`: A list of filter backend classes used to filter job details data.
        - `search_fields`: A list of fields on which the search query can be performed.
        - `pagination_class`: The pagination class used to paginate job details data.
    """
    serializer_class = GetJobsSerializers
    permission_classes = [permissions.AllowAny]
    queryset = JobDetails.objects.filter(deadline__gte=date.today()).order_by('-created')
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count()
        next = None
        previous = None
        paginator = LimitOffsetPagination()
        limit = self.request.query_params.get('limit')
        if limit:
            queryset = paginator.paginate_queryset(queryset, request)
            count = paginator.count
            next = paginator.get_next_link()
            previous = paginator.get_previous_link()
        serializer = self.serializer_class(queryset, many=True, context={"request": request})
        return response.Response(
            {'count': count,
             "next": next,
             "previous": previous,
             "results": serializer.data
             }
        )


class GetJobDetailsView(generics.GenericAPIView):
    """API view to retrieve job details.

    This API view is used to retrieve job details by ID. The returned data includes related data such as country and
    city names, user information, attachments, and more.

    Attributes:
        - `serializer_class`: The serializer class to use for the returned data, which is GetJobsDetailSerializers.
        - `permission_classes`: The permission classes to use for the view, which allow any user to access the data.

    Methods:
        - `get`: A method that retrieves job details by ID and returns the data as a response.
    """
    serializer_class = GetJobsDetailSerializers
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        context = dict()
        job_id = request.GET.get('jobId', None)
        try:
            if job_id:
                job_data = JobDetails.objects.get(id=job_id)
                get_data = self.serializer_class(job_data)
                context = get_data.data
            return response.Response(
                data=context,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            context["message"] = str(e)
            return response.Response(
                data=context,
                status=status.HTTP_400_BAD_REQUEST
            )


class EducationsView(generics.GenericAPIView):
    """
    A generic API view for handling education records.

    Attributes:
        - `permission_classes (list)`: The list of permission classes that the user must have to access this view.
                                In this case, only authenticated users can access this view.

        - `serializer_class (EducationSerializers)`: The serializer class that the view uses to serialize and
                                                deserialize the EducationRecord model.

    Returns:
        Serialized education records in JSON format, with authentication required to access the view. 
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EducationSerializers
    
    def post(self, request):
        """
        Handles HTTP POST requests for creating a new education record.

        Args:
            request (HttpRequest): The request object sent to the server.

        Returns:
            HTTP response with serialized data in JSON format, and status codes indicating whether the request was
            successful or not.

        Raises:
            serializers.ValidationError: If the data in the request is invalid or incomplete.

            Exception: If an error occurs while processing the request.

        Notes:
            This function creates a new education record using the serializer class specified in the `serializer_class`
            attribute of the view. The serializer is first validated and then saved to the database. The `user` field
            of the education record is set to the currently logged-in user.
            If the serializer is not valid, a `serializers.ValidationError` is raised and a response with a status code
            of 400 is returned. If any other error occurs, a response with a status code of 400 is returned along with
            an error message in the `message` field of the response data. If the serializer is valid and the record is
            successfully created, a response with the serialized data and a status code of 201 is returned.
        """

        context = dict()
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            context["data"] = serializer.data
            return response.Response(
                data=context,
                status=status.HTTP_201_CREATED
            )
        except serializers.ValidationError:
            return response.Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            context['message'] = str(e)
            return response.Response(
                data=context,
                status=status.HTTP_400_BAD_REQUEST
            )


