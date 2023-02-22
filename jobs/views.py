from rest_framework import (
    generics, response, status,
    permissions, filters
)
from rest_framework.pagination import LimitOffsetPagination

from datetime import datetime

from core.pagination import CustomPagination

from jobs.models import JobDetails

from job_seekers.models import AppliedJob
from job_seekers.serializers import GetAppliedJobsSerializers

from employers.models import BlackList
from .serializers import (
    GetJobsSerializers,
    GetJobsDetailSerializers,
    AppliedJobSerializers
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


class JobApplicationsView(generics.ListAPIView):
    """
    A view class that returns a list of AppliedJob instances.

    Attributes:
            - `serializer_class`: A serializer class used to serialize the AppliedJob instances.
            - `permission_classes`: A list of permission classes that a user must pass in order to access the view.
            - `queryset`: A QuerySet instance representing the list of AppliedJob instances. The queryset is not
                defined in the class, but it can be defined dynamically in the dispatch method.
            - `filter_backends`: A list of filter backend classes used to filter the queryset.
            - `search_fields`: A list of fields on which the search filtering is applied.
            - `pagination_class`: A pagination class that is used to paginate the result set.

    """
    serializer_class = AppliedJobSerializers
    permission_classes = [permissions.IsAuthenticated]
    queryset = None
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def list(self, request, jobId):
        context = dict()
        if self.request.user.role == "employer":
            try:
                job_instance = JobDetails.objects.get(id=jobId, user=request.user)
                queryset = self.filter_queryset(AppliedJob.objects.filter(job=job_instance).order_by('-created'))
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
            except JobDetails.DoesNotExist:
                return response.Response(
                    data={"job": "Does Not Exist"},
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                context["message"] = e
                return response.Response(
                    data=context,
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
            )


class RecentApplicationsView(generics.ListAPIView):
    """
    A view class that returns a list of AppliedJob instances.

    Attributes:
            - `serializer_class`: A serializer class used to serialize the AppliedJob instances.
            - `permission_classes`: A list of permission classes that a user must pass in order to access the view.
            - `queryset`: A QuerySet instance representing the list of AppliedJob instances. The queryset is not
                defined in the class, but it can be defined dynamically in the dispatch method.
            - `filter_backends`: A list of filter backend classes used to filter the queryset.
            - `search_fields`: A list of fields on which the search filtering is applied.
            - `pagination_class`: A pagination class that is used to paginate the result set.

    """
    serializer_class = AppliedJobSerializers
    permission_classes = [permissions.IsAuthenticated]
    queryset = None
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def list(self, request):
        context = dict()
        if self.request.user.role == "employer":
            try:
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
            except JobDetails.DoesNotExist:
                return response.Response(
                    data={"job": "Does Not Exist"},
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                context["message"] = str(e)
                return response.Response(
                    data=context,
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
            )

    def get_queryset(self, **kwargs):
        """
        A method that returns a queryset of `AppliedJob instances`. It filters the queryset based on the `employer jobs`
        provided in the `request query parameters`.

        Args:
            **kwargs: A dictionary of keyword arguments.

        Returns:
            QuerySet: A filtered queryset of AppliedJob instances.

        """
        job_data = JobDetails.objects.filter(user=self.request.user.id)
        return AppliedJob.objects.filter(job__in=job_data).order_by('-created')


class ApplicationsDetailView(generics.GenericAPIView):
    """
    A view that returns a serialized JobDetail object for a given jobId.

    Parameters:
        - jobId (int): The ID of the job to retrieve details for.

    Returns:
        - data (dict): A dictionary containing the serialized job details.
        - status (int): The HTTP status code of the response.
    """

    serializer_class = GetAppliedJobsSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, applicationId):
        context = dict()
        try:
            if applicationId:
                application_data = AppliedJob.objects.get(id=applicationId)
                get_data = self.serializer_class(application_data)
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

    def patch(self, request, applicationId):
        context = dict()
        try:
            if applicationId:
                action = request.data['action']
                if action == "shortlisted":
                    application_status = AppliedJob.objects.get(id=applicationId)
                    application_status.shortlisted_at=datetime.now()
                    application_status.save()                
                elif action == "rejected":
                    application_status = AppliedJob.objects.get(id=applicationId)
                    application_status.rejected_at=datetime.now()
                    application_status.save() 
                elif action == "blacklisted":
                    application_data = AppliedJob.objects.get(id=applicationId)
                    BlackList.objects.create(user=request.user, blacklisted_user=application_data.user)
                context['message'] = "Successfully " + str(action)
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

