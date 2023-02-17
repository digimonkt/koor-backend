from rest_framework import (
    generics, response, status,
    permissions, filters
)

from core.pagination import CustomPagination
from jobs.models import JobDetails
from .serializers import (
    GetJobsSerializers,
    GetJobsDetailSerializers
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
    pagination_class = CustomPagination


class JobDetailView(generics.GenericAPIView):
    """
    A view that returns a serialized JobDetail object for a given jobId.

    Parameters:
        - jobId (int): The ID of the job to retrieve details for.

    Returns:
        - data (dict): A dictionary containing the serialized job details.
        - status (int): The HTTP status code of the response.
    """

    serializer_class = GetJobsDetailSerializers
    permission_classes = [permissions.AllowAny]

    def get(self, request, jobId):
        context = dict()
        try:
            if jobId:
                job_data = JobDetails.objects.get(id=jobId)
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
