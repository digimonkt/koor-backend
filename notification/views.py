from django.shortcuts import HttpResponse

from datetime import date

from rest_framework import (
    generics, response, permissions, filters
)
from core.pagination import CustomPagination

from job_seekers.models import SavedJob

from notification.models import Notification
from notification.serializers import GetNotificationSerializers


class NotificationView(generics.ListAPIView):
    """
    A view that returns a list of notifications for the authenticated user, filtered by type. Supports pagination with
    limit-offset style.

    Required Attributes:
        - serializer_class: A Django REST Framework serializer class to use for converting notification objects into
            JSON responses.
        - permission_classes: A list of permission classes that define the access control policy for this view.
        - filter_backends: A list of Django REST Framework filter backend classes that perform filtering on the
            queryset.
        - search_fields: A list of model fields that can be searched using the search filter backend.

    Methods:
        - list: A method that returns a JSON response containing a paginated list of notifications for the
            authenticated user, filtered by type.

    Attributes:
        - queryset: The queryset to use for fetching notifications. This attribute is set to None to delay the query
            until the `list` method is called.
    """
    serializer_class = GetNotificationSerializers
    permission_classes = [permissions.IsAuthenticated]
    queryset = None
    filter_backends = [filters.SearchFilter]
    search_fields = ['type']
    pagination_class = CustomPagination

    def list(self, request):
        """
        Return a JSON response containing a paginated list of notifications for the authenticated user, filtered by
        type.

        If a 'limit' query parameter is provided, pagination is performed using a limit-offset style. Otherwise, all
        notifications for the user are returned.

        Arguments:
            - `request`: The incoming HTTP request.

        Returns:
            - A Django REST Framework Response object containing a JSON payload with the following keys:
            - 'count': The total number of notifications in the response.
            - 'next': A URL for the next page of results, or None if there is no next page.
            - 'previous': A URL for the previous page of results, or None if there is no previous page.
            - 'results': A list of notification objects, serialized as JSON.
        """
        queryset = Notification.objects.filter(user=self.request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, context={"request": request})
        return response.Response(serializer.data)


def ExpiredSavedJobs():
    """
    Sends notifications to users who have saved job postings that have passed their deadline and have not been notified
    yet.

    Returns a HTTP response object indicating that all notifications have been sent.
    """

    saved_job_data = SavedJob.objects.filter(job__deadline__lte=date.today(), notified=False)
    Notification.objects.bulk_create(
        [
            Notification(
                user=saved_job.user,
                job=saved_job.job,
                notification_type='expired_save_job',
            ) for saved_job in saved_job_data
        ]
    )
    if saved_job.user.email:
        email_context = dict()
        if saved_job.user.name:
            user_name = saved_job.user.name
        else:
            user_name = saved_job.user.email
        email_context["yourname"] = user_name
        email_context["notification_type"] = "expired save job"
        email_context["job_instance"] = saved_job.job
        get_email_object(
            subject=f'Notification for expired save job',
            email_template_name='email-templates/send-notification.html',
            context=email_context,
            to_email=[job_filter.user.email, ]
        )
    saved_job_data = SavedJob.objects.filter(
        job__deadline__lte=date.today(), notified=False
    ).update(notified=True)
    return HttpResponse("done")
