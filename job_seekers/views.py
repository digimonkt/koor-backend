from django.shortcuts import get_object_or_404

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
    UpdateAboutSerializers, GetJobsDetailSerializers
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
    queryset = JobDetails.objects.all().order_by('-created')
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
