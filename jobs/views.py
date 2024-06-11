from django.db.models import (
    Value, F, Case, When, IntegerField, Q,
    Count
)


from rest_framework import (
    generics, response, status,
    permissions, filters, serializers
)

from datetime import datetime, date

from django_filters import rest_framework as django_filters

from core.emails import get_email_object
from core.pagination import CustomPagination

from jobs.models import (
    JobDetails, JobFilters, JobShare,
    JobCategory, JobSubCategory
)
from tenders.models import (
    TenderCategory
)

from job_seekers.models import AppliedJob
from jobs.serializers import (
    GetAppliedJobsSerializers, JobCategorySerializer
)

from notification.models import Notification

from employers.models import BlackList

from .serializers import (
    GetJobsSerializers,
    GetJobsDetailSerializers,
    AppliedJobSerializers,
    JobFiltersSerializers,
    GetJobFiltersSerializers,
    ShareCountSerializers
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
    queryset = None
    filter_backends = [filters.SearchFilter, django_filters.DjangoFilterBackend]
    filterset_class = JobDetailsFilter
    search_fields = [
        'title', 'user__name'
    ]
    # search_fields = [
    #     'title', 'description',
    #     'skill__title', 'highest_education__title',
    #     'job_category__title', 'job_sub_category__title',
    #     'country__title', 'city__title', 'user__name'
    # ]
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
        jobSubCategory = request.GET.getlist('jobSubCategory')
        fullTime = request.GET.get('fullTime')
        partTime = request.GET.get('partTime')
        contract = request.GET.get('contract')
        job_type = None
        if fullTime:
            if job_type:
                job_type = job_type | Q(is_full_time=True)
            else:
                job_type = Q(is_full_time=True)
        if partTime:
            if job_type:
                job_type = job_type | Q(is_part_time=True)
            else:
                job_type = Q(is_part_time=True)
        if contract:
            if job_type:
                job_type = job_type | Q(has_contract=True)
            else:
                job_type = Q(has_contract=True)
        if job_type:
            queryset = queryset.filter(job_type)
        if jobCategory  and jobSubCategory in ["", None, []]:
            queryset = queryset.filter(job_category__title__in=jobCategory).distinct()
        if jobSubCategory:
            queryset = queryset.filter(job_sub_category__title__in=jobSubCategory).distinct()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context=context)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, context=context)
        return response.Response(serializer.data)

    def get_queryset(self, **kwargs):
        """
        Returns the queryset of applied jobs for the authenticated user.

        This method returns a queryset of AppliedJob objects for the authenticated user, ordered by their creation date
        in descending order.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            A queryset of AppliedJob objects for the authenticated user, ordered by their creation date in descending
            order.
        """
        order_by = None
        filters = Q(is_removed=False)
        if 'filter_by' in self.request.GET:
            filter_by = self.request.GET['filter_by']
            if filter_by == "active": filters = filters & Q(deadline__gte=date.today())
            if filter_by == 'expired': filters = filters & Q(deadline__lt=date.today())

        if 'search_by' in self.request.GET:
            search_by = self.request.GET['search_by']
            if search_by == 'salary':
                order_by = 'budget_amount'
            elif search_by == 'expiration':
                order_by = 'deadline'
            elif search_by == 'created_at':
                order_by = 'start_date'
            if order_by:
                if 'order_by' in self.request.GET:
                    if 'descending' in self.request.GET['order_by']:
                        return JobDetails.objects.filter(
                            # deadline__gte=date.today(),
                            # is_removed=False,
                            status="active"
                        ).filter(filters).order_by("-" + str(order_by), '-created')
                    else:
                        return JobDetails.objects.filter(
                            # deadline__gte=date.today(),
                            # is_removed=False,
                            status="active"
                        ).filter(filters).order_by(str(order_by), 'created')
                else:
                    return JobDetails.objects.filter(
                        # deadline__gte=date.today(),
                        # is_removed=False,
                        status="active"
                    ).filter(filters).order_by(str(order_by, 'created'))
        return JobDetails.objects.filter(
            # deadline__gte=date.today(),
            # is_removed=False,
            status="active"
        ).filter(filters)


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
        context = dict()
        try:
            if request.user.is_authenticated:
                context = {"user": request.user}
            if jobId:
                try:
                    job_data = JobDetails.objects.get(slug=jobId)
                except JobDetails.DoesNotExist:
                    try:
                        job_data = JobDetails.objects.get(id=jobId)
                    except JobDetails.DoesNotExist:
                        return response.Response(
                            data={"job": "Does Not Exist"},
                            status=status.HTTP_404_NOT_FOUND
                        )
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
    pagination_class = CustomPagination

    def list(self, request, jobId):
        context = dict()
        if self.request.user.role == "employer":
            try:
                job_instance = JobDetails.objects.get(id=jobId, user=request.user)
                filters = Q(job=job_instance)
                filter_list = self.request.GET.getlist('filter')
                blacklisted_user_list = []
                for data in BlackList.objects.all():
                    blacklisted_user_list.append(data.blacklisted_user)
                for filter_data in filter_list:
                    if filter_data == "rejected": filters = filters & ~Q(rejected_at=None)
                    if filter_data == "shortlisted": filters = filters & ~Q(shortlisted_at=None)
                    if filter_data == "planned_interviews": filters = filters & ~Q(interview_at=None)
                    if filter_data == "blacklisted": filters = filters & Q(user__in=blacklisted_user_list)
                queryset = self.filter_queryset(AppliedJob.objects.filter(filters))
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page, many=True, context={"request": request})
                    serialized_response = self.get_paginated_response(serializer.data)
                    serialized_response.data['rejected_count'] = AppliedJob.objects.filter(job=job_instance).filter(
                        ~Q(rejected_at=None)).count()
                    serialized_response.data['shortlisted_count'] = AppliedJob.objects.filter(job=job_instance).filter(
                        ~Q(shortlisted_at=None)).count()
                    serialized_response.data['planned_interview_count'] = AppliedJob.objects.filter(
                        job=job_instance).filter(~Q(interview_at=None)).count()
                    user_list = []
                    for data in AppliedJob.objects.filter(job=job_instance):
                        user_list.append(data.user)
                    serialized_response.data['blacklisted_count'] = BlackList.objects.filter(
                        blacklisted_user__in=user_list).order_by('blacklisted_user').distinct(
                        'blacklisted_user').count()
                    return response.Response(data=serialized_response.data, status=status.HTTP_200_OK)
                serializer = self.get_serializer(queryset, many=True, context={"request": request})
                return response.Response(serializer.data)
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
    search_fields = ['job__title', 'user__email', 'user__name']
    pagination_class = CustomPagination

    def list(self, request):
        context = dict()
        if self.request.user.role == "employer":
            try:
                queryset = self.filter_queryset(self.get_queryset())
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page, many=True, context={"request": request})
                    return self.get_paginated_response(serializer.data)
                serializer = self.get_serializer(queryset, many=True, context={"request": request})
                return response.Response(serializer.data)
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
        
        if 'filterBy' in self.request.GET:
            filter_by = self.request.GET['filterBy']
            if filter_by == "shortlisted":
                return AppliedJob.objects.filter(job__in=job_data).filter(~Q(shortlisted_at=None))
            elif filter_by == "interview":
                return AppliedJob.objects.filter(job__in=job_data).filter(~Q(interview_at=None))
            elif filter_by == "rejected":
                return AppliedJob.objects.filter(job__in=job_data).filter(~Q(rejected_at=None))
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

    def put(self, request, applicationId, action):
        context = dict()
        try:
            if applicationId:
                application_status = AppliedJob.objects.get(id=applicationId)
                if application_status.job.user == request.user:
                    message = "Successfully "
                    if action == "shortlisted":
                        if application_status.shortlisted_at:
                            message = "Already "
                        else:
                            application_status.shortlisted_at = datetime.now()
                            application_status.save()
                            if application_status.user.get_notification:
                                Notification.objects.create(
                                    user=application_status.user, application=application_status,
                                    notification_type='shortlisted', created_by=request.user, job=application_status.job
                                )
                                if application_status.user.email:
                                    email_context = dict()
                                    if application_status.user.name:
                                        user_name = application_status.user.name
                                    else:
                                        user_name = application_status.user.email
                                    email_context["yourname"] = user_name
                                    email_context["notification_type"] = "shortlisted jobs"
                                    email_context["job_instance"] = application_status.job
                                    email_context["job_link"] = Common.FRONTEND_BASE_URL + "/jobs/details/" + str(application_status.job.slug)
                                    if application_status.user.get_email:
                                        get_email_object(
                                            subject=f'Notification for shortlisted job',
                                            email_template_name='email-templates/send-notification-old.html',
                                            context=email_context,
                                            to_email=[application_status.user.email, ]
                                        )
                    elif action == "rejected":
                        if application_status.rejected_at:
                            message = "Already "
                        else:
                            application_status.shortlisted_at = None
                            application_status.rejected_at = datetime.now()
                            application_status.save()
                            
                            if application_status.user.get_notification:
                                Notification.objects.create(
                                    user=application_status.user, application=application_status,
                                    notification_type='rejected', created_by=request.user, job=application_status.job
                                )
                                if application_status.user.email:
                                    email_context = dict()
                                    if application_status.user.name:
                                        user_name = application_status.user.name
                                    else:
                                        user_name = application_status.user.email
                                    email_context["yourname"] = user_name
                                    email_context["notification_type"] = "rejected job"
                                    email_context["job_instance"] = application_status.rejected_at
                                    email_context["job_link"] = Common.FRONTEND_BASE_URL + "/jobs/details/" + str(application_status.rejected_at.slug)
                                    if application_status.user.get_email:
                                        get_email_object(
                                            subject=f'Notification for rejected job',
                                            email_template_name='email-templates/send-notification-old.html',
                                            context=email_context,
                                            to_email=[application_status.user.email, ]
                                        )
                                        
                    elif action == "blacklisted":
                        if 'reason' in request.data:
                            if BlackList.objects.filter(user=request.user, blacklisted_user=application_status.user):
                                message = "Already "
                            else:
                                BlackList.objects.create(
                                    user=request.user,
                                    blacklisted_user=application_status.user,
                                    reason=request.data['reason']
                                )
                        else:
                            return response.Response(
                                data={"message": ["Please select a reason"]},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                    elif action == "planned_interviews":
                        if application_status.rejected_at is None:
                            if 'interview_at' in request.data:
                                interview_at_str = request.data['interview_at']
                                current_datetime = datetime.now()
                                try:
                                    interview_at_datetime = datetime.strptime(interview_at_str, '%Y-%m-%dT%H:%M:%S')
                                except ValueError:
                                    interview_at_datetime = datetime.strptime(interview_at_str, '%Y-%m-%dT%H:%M')
                                current_datetime = datetime.now()
                                if interview_at_datetime < current_datetime:
                                    return response.Response(
                                        data={"message": ["Interview date in invalid."]},
                                        status=status.HTTP_400_BAD_REQUEST
                                    )
                                else:
                                    if application_status.shortlisted_at is None:
                                        application_status.shortlisted_at = datetime.now()
                                    application_status.interview_at = request.data['interview_at']
                                    application_status.save()
                                    if application_status.user.get_notification:
                                        Notification.objects.create(
                                            user=application_status.user, application=application_status,
                                            notification_type='planned_interviews', created_by=request.user, job=application_status.job
                                        )
                                        if application_status.user.email:
                                            email_context = dict()
                                            if application_status.user.name:
                                                user_name = application_status.user.name
                                            else:
                                                user_name = application_status.user.email
                                            email_context["yourname"] = user_name
                                            email_context["notification_type"] = "interview planned"
                                            email_context["job_instance"] = application_status.job
                                            email_context["job_link"] = Common.FRONTEND_BASE_URL + "/jobs/details/" + str(application_status.job.slug)
                                            if application_status.user.get_email:
                                                get_email_object(
                                                    subject=f'Notification for interview planned',
                                                    email_template_name='email-templates/new/notification.html',
                                                    # email_template_name='email-templates/send-notification-old.html',
                                                    context=email_context,
                                                    to_email=[application_status.user.email, ]
                                                )
                            else:
                                return response.Response(
                                    data={"interview_at": ["This field is requeired."]},
                                    status=status.HTTP_400_BAD_REQUEST
                                )
                        else:
                            return response.Response(
                                data={"message": ["Application already rejected."]},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                    context['message'] = str(message) + str(action)
                    return response.Response(
                        data=context,
                        status=status.HTTP_200_OK
                    )
                else:
                    context['message'] = ["You do not have permission to perform this action."]
                    return response.Response(
                        data=context,
                        status=status.HTTP_401_UNAUTHORIZED
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
    # queryset = JobDetails.objects.all()
    queryset = JobDetails.objects.filter(deadline__gte=date.today(), is_removed=False, status="active")
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
            job_instance = JobDetails.objects.get(slug=jobId)
            annotated_job_details = JobDetails.objects.filter(deadline__gte=date.today(), is_removed=False, status="active").filter(~Q(id=job_instance.id)).annotate(
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
                        job_sub_category__in=job_instance.job_sub_category.all(),
                        then=F('matches') + 1
                    ),
                    default=F('matches'),
                    output_field=IntegerField()
                )
            ).annotate(
                matches=Case(
                    When(
                        duration=job_instance.duration,
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
            jobs = annotated_job_details.filter(matches=4).order_by('-matches').distinct('matches')
            if jobs.count() == 0:
                jobs = annotated_job_details.order_by('-matches').distinct('matches')
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


class JobShareView(generics.GenericAPIView):
    """
    A view for updating job sharing details for a specific job on a particular platform.

    This view allows updating the number of shares for a job on a specific platform, such as `WhatsApp`, `Telegram`,
    `Facebook`, or Mail. It takes the jobId and platform as URL parameters and uses a `PUT` request to update the
    corresponding `JobShare` instance. If the `JobDetails` or `JobShare` instance does not exist, it returns a
    `404 Not Found` response. If there is any other error, it returns a `400 Bad Request` response.

    Methods:
        - `put(request, jobId, platform)`: Updates the number of shares for a job on a specific platform.

    Args:
        - `request (Request)`: The HTTP request object.
        - `jobId (int)`: The ID of the job to update the sharing details for.
        - `platform (str)`: The name of the platform to update the sharing details on.

    Returns:
        - `Response`: A response object with status code and message.

    Raises:
        - `None`.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = ShareCountSerializers

    def get(self, request, jobId):
        context = dict()
        try:
            job_instance = JobDetails.objects.get(id=jobId)
            queryset = JobShare.objects.get(job=job_instance)
            serializer = self.get_serializer(queryset)
            return response.Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            context['message'] = str(e)
            return response.Response(
                data=context,
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, jobId, platform):
        context = dict()
        try:
            job_instance = JobDetails.objects.get(id=jobId)
            job_share_instance = JobShare.objects.get(job=job_instance)
            if platform == "whatsapp":
                job_share_instance.whatsapp = job_share_instance.whatsapp + 1
                job_share_instance.save()
            elif platform == "telegram":
                job_share_instance.telegram = job_share_instance.telegram + 1
                job_share_instance.save()
            elif platform == "facebook":
                job_share_instance.facebook = job_share_instance.facebook + 1
                job_share_instance.save()
            elif platform == "mail":
                job_share_instance.mail = job_share_instance.mail + 1
                job_share_instance.save()
            elif platform == "linked_in":
                job_share_instance.linked_in = job_share_instance.linked_in + 1
                job_share_instance.save()
            elif platform == "direct_link":
                job_share_instance.direct_link = job_share_instance.direct_link + 1
                job_share_instance.save()
            return response.Response(
                data={"message": "Share details updated"},
                status=status.HTTP_200_OK
            )
        except JobShare.DoesNotExist:
            return response.Response(
                data={"message": "Job share does not exist with this job."},
                status=status.HTTP_404_NOT_FOUND
            )
        except JobDetails.DoesNotExist:
            return response.Response(
                data={"jobId": "Does Not Exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["message"] = str(e)
            return response.Response(
                data=context,
                status=status.HTTP_400_BAD_REQUEST
            )


class JobCategoryView(generics.ListAPIView):
    """
    A view for retrieving the top job categories along with their counts of associated jobs and talents.

    Attributes:
        - `permission_classes`: A list of permission classes applied to the view.
        - `queryset`: The queryset for the view. (Note: It is set to None in this case.)

    Methods:
        - `list(self, request)`: Handles the GET request and returns the response with the top job categories,
          along with the counts of associated jobs and talents.

    Returns:
        A response with a JSON payload containing the following structure:
        {
            "jobs": [
                {
                    "title": <job_category_title>,
                    "count": <job_category_count>
                },
                ...
            ],
            "talents": [
                {
                    "title": <talent_category_title>,
                    "count": <talent_category_count>
                },
                ...
            ]
        }
    """

    permission_classes = [permissions.AllowAny]
    queryset = None

    def list(self, request):
        """
        Handles the GET request and returns the response with the top job categories,
        along with the counts of associated jobs and talents.

        Returns:
        A response with a JSON payload containing the top job categories and their counts of associated jobs and talents.
        """
        context = dict()
        jobs = []
        talents = []
        tenders = []

        # Retrieve the top job categories and their counts of associated jobs
        all_jobs = JobCategory.objects.annotate(
            category_count=Count(
                'jobs_jobdetails_job_category',
                distinct=True,
                filter=Q(jobs_jobdetails_job_category__is_removed=False, jobs_jobdetails_job_category__status="active")
            )
        ).order_by('-category_count')[:5]
        # Retrieve the top job categories and their counts of associated talents
        all_talents = JobCategory.objects.annotate(
            category_count=Count(
                'jobs_jobsubcategory_categories__job_seekers_categories_categories__user',
                distinct=True,
                filter=Q(
                    jobs_jobsubcategory_categories__job_seekers_categories_categories__user__job_seekers_jobpreferences_user__display_in_search=True,
                    jobs_jobsubcategory_categories__job_seekers_categories_categories__user__is_active=True,
                    jobs_jobsubcategory_categories__is_removed=False,
                    jobs_jobsubcategory_categories__isnull=False,
                )
            )
        ).order_by('-category_count')[:5]

        # Retrieve the top tenders categories and their counts of associated tender
        all_tenders = TenderCategory.objects.annotate(
            category_count=Count(
                'tenders_tenderdetails_tender_category',
                distinct=True,
                filter=Q(tenders_tenderdetails_tender_category__is_removed=False, tenders_tenderdetails_tender_category__status='active')
            )
        ).order_by('-category_count')[:5]

        # Prepare the jobs list with title and count information
        for category in all_jobs:
            jobs.append({"id": category.id, "title": category.title, "count": category.category_count})

        # Prepare the talents list with title and count information
        for category in all_talents:
            talents.append({"id": category.id, "title": category.title, "count": category.category_count})
            
        # Prepare the tenders list with title and count information
        for category in all_tenders:
            tenders.append({"id": category.id, "title": category.title, "count": category.category_count})

        # Populate the context dictionary with jobs and talents information
        context['jobs'] = jobs
        context['talents'] = talents
        context['tenders'] = tenders
        
        return response.Response(
            data=context,
            status=status.HTTP_200_OK
        )

class PopularJobCategoryView(generics.ListAPIView):
    """
    A view for retrieving the popular job categories along with their counts.

    Attributes:
        - `permission_classes`: A list of permission classes applied to the view.
        - `queryset`: The queryset for the view. (Note: It is set to None in this case.)

    Methods:
        - `list(self, request)`: Handles the GET request and returns the response with the popular job categories
          and their counts.

    Returns:
        A response with a JSON payload containing the following structure:
        {
            "job_categories": [
                {
                    "title": <job_category_title>,
                    "count": <job_category_count>
                },
                ...
            ]
        }
    """

    permission_classes = [permissions.AllowAny]
    queryset = None

    def list(self, request):
        """
        Handles the GET request and returns the response with the popular job categories and their counts.

        Returns:
        A response with a JSON payload containing the popular job categories and their counts.
        """
        job_categories = []

        # Retrieve the popular job categories and their counts
        most_used_categories = JobDetails.objects.filter(is_removed=False, status="active"
                        ).values('job_category__id', 'job_category__title').annotate(
            category_count=Count('job_category')).order_by('-category_count')
        # Prepare the job categories list with title and count information
        all_job_category_id = []
        job_category = JobCategory.objects.all()
        for cat_id in job_category:
            all_job_category_id.append(cat_id.id)
        for category in most_used_categories:
            if category['job_category__id'] in all_job_category_id:
                job_categories.append(
                    {
                        "id": category['job_category__id'],
                        "title": category['job_category__title'],
                        "count": category['category_count']
                    }
                )
        total_jobs = JobDetails.objects.filter(is_removed=False, status="active").count()
        return response.Response(
            # data= job_categories,
            data= {"total_jobs":total_jobs , 'job_categories':job_categories} ,
            status=status.HTTP_200_OK
        )
        
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from koor.config.common import Common
import base64


class DownloadImage(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        context = dict()
        file_path = request.GET.get('file_path', None)
        file_path = file_path.split("media")
        new_file_path = Common.MEDIA_ROOT + file_path[1]
        encoded_string = ""
        with open(new_file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        context['base_image'] = encoded_string
        return response.Response(
            data=context,
            status=status.HTTP_200_OK
        )
