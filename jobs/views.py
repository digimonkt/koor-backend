from django.db.models import Value, F, Case, When, IntegerField

from rest_framework import (
    generics, response, status,
    permissions, filters, serializers
)
from rest_framework.pagination import LimitOffsetPagination

from datetime import datetime, date

from django_filters import rest_framework as django_filters

from core.pagination import CustomPagination

from jobs.models import JobDetails, JobFilters

from job_seekers.models import AppliedJob
from jobs.serializers import GetAppliedJobsSerializers

from employers.models import BlackList

from .serializers import (
    GetJobsSerializers,
    GetJobsDetailSerializers,
    AppliedJobSerializers,
    JobFiltersSerializers,
    GetJobFiltersSerializers
)
from .filters import JobDetailsFilter


class JobSearchView(generics.ListAPIView):
    """
    A view for searching and filtering job details.

    This view allows for searching and filtering job details based on various criteria, including job category and job
    title.
    The view returns a paginated list of jobs matching the specified criteria.

    Attributes:
        - `serializer_class`: A Django Rest Framework serializer class for serializing `JobDetails` objects.
        - `permission_classes`: A list of Django Rest Framework permission classes that define the permission policy for
                                the view.
        - `queryset`: A Django QuerySet that defines the base set of `JobDetails` objects for the view.
        - `filter_backends`: A list of Django Rest Framework filter backend classes that provide filtering and search
                             functionality.
        - `filterset_class`: A Django FilterSet class used for filtering the queryset.
        - `search_fields`: A list of fields that can be searched for a given query.
        - `pagination_class`: A Django Rest Framework pagination class for paginating the results of the view.

    Methods:
        - `list(self, request)`: Returns a paginated list of job details that match the specified criteria.

    Returns:
        - A paginated list of job details that match the specified criteria.
    """

    serializer_class = GetJobsSerializers
    permission_classes = [permissions.AllowAny]
    queryset = JobDetails.objects.filter(deadline__gte=date.today())
    filter_backends = [filters.SearchFilter, django_filters.DjangoFilterBackend]
    filterset_class = JobDetailsFilter
    search_fields = ['title']
    pagination_class = CustomPagination

    def list(self, request):
        """
        Return a paginated list of job details matching the specified search and filter criteria.

        This method filters the queryset based on the search and filter criteria provided in the request.
        It returns a paginated list of job details that match the specified criteria.

        Parameters:
            - `self`: The current instance of the class.
            - `request`: The HTTP request object that contains the search and filter criteria.

        Returns:
            - A paginated list of job details that match the specified search and filter criteria.
        """
        context = dict()
        if request.user.is_authenticated:
            context = {"user": request.user}

        queryset = self.filter_queryset(self.get_queryset())
        jobCategory = request.GET.getlist('jobCategory')
        if jobCategory:
            queryset = queryset.filter(job_category__title__in=jobCategory).distinct()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context=context)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, context=context)
        return response.Response(serializer.data)


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
        response_context = dict()
        try:
            if request.user:
                context = {"user": request.user}
            if jobId:
                job_data = JobDetails.objects.get(id=jobId)
                get_data = self.serializer_class(job_data, context=context)
                response_context = get_data.data
            return response.Response(
                data=response_context,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            response_context["message"] = str(e)
            return response.Response(
                data=response_context,
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
                queryset = self.filter_queryset(AppliedJob.objects.filter(job=job_instance))
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
        return AppliedJob.objects.filter(job__in=job_data)


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
                    application_status.shortlisted_at = datetime.now()
                    application_status.save()
                elif action == "rejected":
                    application_status = AppliedJob.objects.get(id=applicationId)
                    application_status.rejected_at = datetime.now()
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


class JobSuggestionView(generics.ListAPIView):
    serializer_class = GetJobsSerializers
    permission_classes = [permissions.AllowAny]
    queryset = JobDetails.objects.all()
    filter_backends = [filters.SearchFilter, django_filters.DjangoFilterBackend]
    filterset_class = JobDetailsFilter
    search_fields = ['title']
    pagination_class = CustomPagination

    def list(self, request, jobId):
        context = dict()
        if request.user:
            context = {"user": request.user}
        queryset = self.filter_queryset(self.get_queryset())
        try:
            job_instance = JobDetails.objects.get(id=jobId)
            annotated_job_details = JobDetails.objects.annotate(
                matches=Value(0)
            ).annotate(
                matches=Case(
                    When(
                        budget_amount=job_instance.budget_amount,
                        then=F('matches') + 1
                    ),
                    default=F('matches'),
                    output_field=IntegerField()
                )
            ).annotate(
                matches=Case(
                    When(
                        skill__in=job_instance.skill.all(),
                        then=F('matches') + 1
                    ),
                    default=F('matches'),
                    output_field=IntegerField()
                )
            ).annotate(
                matches=Case(
                    When(
                        job_category__in=job_instance.job_category.all(),
                        then=F('matches') + 1
                    ),
                    default=F('matches'),
                    output_field=IntegerField()
                )
            ).annotate(
                matches=Case(
                    When(
                        working_days=job_instance.working_days,
                        then=F('matches') + 1
                    ),
                    default=F('matches'),
                    output_field=IntegerField()
                )
            ).annotate(
                matches=Case(
                    When(
                        highest_education=job_instance.highest_education,
                        then=F('matches') + 1
                    ),
                    default=F('matches'),
                    output_field=IntegerField()
                )
            )
            jobs = annotated_job_details.filter(matches=4)
            if jobs.count() == 0:
                jobs = annotated_job_details.order_by('-matches')
            page = self.paginate_queryset(jobs)
            if page is not None:
                serializer = self.get_serializer(page, many=True, context=context)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(jobs, many=True, context=context)
            return response.Response(serializer.data)
        except JobDetails.DoesNotExist:
            return response.Response(
                data={"job": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )


class JobFilterView(generics.GenericAPIView):
    """
    `JobFilterView` is a class-based view that inherits from the GenericAPIView class of the `Django REST Framework`.
    It defines the serializer_class attribute as `JobFiltersSerializers` and permission_classes as `IsAuthenticated`.

    Attributes:
        - `serializer_class (class)`: The serializer class to be used for the view.
        - `permission_classes (list)`: A list of permission classes that the user must have in order to access the view.

    Usage:
        - This view can be used to save JobFilters objects in the database. The user must be authenticated to access
            this view.
        - When a `POST` request is made to this view, it will create a `new JobFilters` object in the database with the
            data provided in the request body.
        - The serializer class is used to validate the data and convert it to a JobFilters object.
    """

    serializer_class = JobFiltersSerializers
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        post is a method of the `JobFilterView` class that handles HTTP POST requests to save `JobFilters` objects in
        the database.

        Args:
            - `request (HttpRequest)`: An HTTP POST request containing the data for the JobFilters object.

        Returns:
            - `HttpResponse`: A JSON response containing either the serialized JobFilters object and a status code of
                `201 CREATED`, or a JSON error response with a status code of `400 BAD REQUEST`.

        Raises:
            - `ValidationError`: If the serializer fails to validate the request data.

        Usage:
            - This method is used to handle POST requests made to the JobFilterView view. It first creates a context
                dictionary to store any additional data to be passed to the serializer.
            - It then creates an instance of the JobFiltersSerializers class using the request data.
            - The serializer is validated, and if it is valid, the JobFilters object is saved to the database with the
                authenticated user who made the request.
            - A JSON response containing the serialized JobFilters object is returned with a status code of 201 CREATED.
            - If the serializer fails to validate the data, a JSON error response is returned with a status code of 400
                BAD REQUEST.
        """

        context = dict()
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return response.Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        except serializers.ValidationError:
            return response.Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request):
        """
        get is a method of the `JobFilterView` class that handles HTTP GET requests to retrieve JobFilters objects
        saved by a particular user.

        Args:
            - `request (HttpRequest)`: An HTTP GET request.

        Returns:
            - `HttpResponse`: A JSON response containing a serialized list of JobFilters objects associated with the
                authenticated user who made the request and a status code of 200 OK, or a JSON error response with a
                status code of 400 BAD REQUEST.

        Raises:
            - `Exception`: If there is an error retrieving the JobFilters objects.

        Usage:
            - This method is used to handle GET requests made to the SaveFilterView view. It first creates a context
                dictionary to store any additional data to be passed to the serializer.
            - It then retrieves all JobFilters objects associated with the authenticated user who made the request
                using the filter method.
            - The data is serialized using the GetJobFiltersSerializers class and returned as a JSON response with a
                status code of 200 OK.
            - If there is an error retrieving the data, a JSON error response is returned with a status code of 400
                BAD REQUEST.
        """

        context = dict()
        try:
            job_filter_data = JobFilters.objects.filter(user=request.user)
            get_data = GetJobFiltersSerializers(job_filter_data, many=True)
            return response.Response(
                data=get_data.data,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            context["error"] = str(e)
            return response.Response(
                data=context,
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, filterId):
        """
        A function to delete a job filter instance for a job seeker user.

        Args:
        - `request (HttpRequest)`: An HTTP request object.
        - `filterId (int)`: An integer representing the ID of the job filter instance to be deleted.

        Returns:
        - A Response object with a JSON representation of a message indicating the result of the operation and the HTTP
            status code.

        Raises:
        - `JobFilters.DoesNotExist`: If the job filter instance with the given filterId and user does not exist.
        - `Exception`: If there is any other error during the deletion process.
        """

        context = dict()
        if request.user.role == "job_seeker":
            try:
                JobFilters.all_objects.get(id=filterId, user=request.user).delete(soft=False)
                context['message'] = "Filter Removed"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except JobFilters.DoesNotExist:
                return response.Response(
                    data={"filterId": "Does Not Exist"},
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

    def patch(self, request, filterId):
        """
        A function to partially update a job filter instance for a job seeker user.

        Args:
        - `request (HttpRequest)`: An HTTP request object.
        - `filterId (int)`: An integer representing the ID of the job filter instance to be updated.

        Returns:
        - A Response object with a JSON representation of a message indicating the result of the operation and the HTTP
            status code.

        Raises:
        - `JobFilters.DoesNotExist`: If the job filter instance with the given filterId and user does not exist.
        - `Exception`: If there is any other error during the partial update process.
        """

        context = dict()
        if self.request.user.role == "job_seeker":
            try:
                filter_instance = JobFilters.all_objects.get(id=filterId, user=request.user)
                serializer = self.serializer_class(data=request.data, instance=filter_instance, partial=True)
                try:
                    serializer.is_valid(raise_exception=True)
                    if serializer.update(filter_instance, serializer.validated_data):
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
            except JobFilters.DoesNotExist:
                return response.Response(
                    data={"filterId": "Does Not Exist"},
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
