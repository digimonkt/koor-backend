from django.core.handlers.wsgi import WSGIHandler
from django.core.signals import request_finished
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import (
    generics, response, status,
    permissions, serializers, filters
)

from core.pagination import CustomPagination

from jobs.models import JobDetails, JobFilters
from jobs.serializers import GetJobsSerializers

from notification.models import Notification

from user_profile.models import EmployerProfile
from users.models import User

from .serializers import (
    UpdateAboutSerializers,
    CreateJobsSerializers,
    UpdateJobSerializers
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
        if self.request.user.role == "employer":
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
        else:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
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
    search_fields = [
        'title', 'description',
        'skill__title', 'highest_education__title',
        'job_category__title', 'country__title',
        'city__title'
    ]
    pagination_class = CustomPagination
    

    def list(self, request):
        context = dict()
        if self.request.user.role == 'employer':
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True, context={"user": request.user})
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True, context={"user": request.user})
            return response.Response(serializer.data)
        else:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
            )

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
                request_finished.connect(my_callback, sender=WSGIHandler, dispatch_uid='notification_trigger_callback')
                return response.Response(
                    data=context,
                    status=status.HTTP_201_CREATED
                )
            else:
                context['message'] = "You do not have permission to perform this action."
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
        return JobDetails.objects.filter(user=user_data)

    def put(self, request, jobId):
        """
        Update an existing job instance with the provided request data.

        Args:
            - `request`: An instance of the Django Request object.

        Returns:
            An instance of the Django Response object with a JSON-encoded message indicating whether the job instance
            was updated successfully or not.

        Raises:
            - `Http404`: If the JobDetails instance with the provided jobId does not exist.

        Notes:
            This method requires a jobId to be included in the request data, and will only update the job if the
            authenticated user matches the user associated with the job instance. The UpdateJobSerializers class is
            used to serialize the request data and update the job instance. If the serializer is invalid or the user
            does not have permission to update the job instance, an appropriate error response is returned.
        """
        context = dict()
        try:
            job_instance = JobDetails.objects.get(id=jobId)
            if request.user == job_instance.user:
                serializer = UpdateJobSerializers(data=request.data, instance=job_instance, partial=True)
                try:
                    serializer.is_valid(raise_exception=True)
                    if serializer.update(job_instance, serializer.validated_data):
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
            else:
                context['message'] = "You do not have permission to perform this action."
                return response.Response(
                    data=context,
                    status=status.HTTP_401_UNAUTHORIZED
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


def my_callback(sender, **kwargs):
    """
    A callback function that generates notifications for job filters matching the job details of a recently finished
    request.

    Args:
        - `sender`: The sender of the signal, typically a Django web application.
        - `**kwargs`: Additional keyword arguments provided by the signal.

    Returns:
        - None.

    Functionality:
        - Fetches the first JobDetails instance from the database.
        - Filters JobFilters instances based on the job details, including `country`, `city`, `job category`,
            `employment type`, and `working days`.
        - Creates Notification instances for each matching JobFilters instance.
        - Disconnects this callback function from the request_finished signal after execution.
    """

    job_instance = JobDetails.objects.first()
    job_filter_data = JobFilters.objects.filter(
        is_notification=True
    ).filter(
        Q(country=job_instance.country) | Q(country=None)
    ).filter(
        Q(city=job_instance.city) | Q(city=None)
    ).filter(
        Q(job_category__in=[(job_category_value) for job_category_value in job_instance.job_category.all()]) | Q(
            job_category=None)
    ).filter(
        Q(is_full_time=job_instance.is_full_time) | Q(is_full_time=None)
    ).filter(
        Q(is_part_time=job_instance.is_part_time) | Q(is_part_time=None)
    ).filter(
        Q(has_contract=job_instance.has_contract) | Q(has_contract=None)
    ).filter(
        Q(working_days=job_instance.working_days) | Q(working_days=None)
    )

    Notification.objects.bulk_create(
        [
            Notification(
                user=job_filter.user,
                job_filter=job_filter,
                job=job_instance,
                notification_type='advance_filter',
                created_by=job_instance.user
            ) for job_filter in job_filter_data
        ]
    )
    request_finished.disconnect(my_callback, sender=WSGIHandler, dispatch_uid='notification_trigger_callback')
