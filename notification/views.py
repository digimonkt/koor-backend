from django.shortcuts import HttpResponse

from datetime import date

from rest_framework import (
    generics, response, status,
    permissions, filters
)
from koor.config.common import Common
from core.emails import get_email_object
from core.pagination import CustomPagination

from job_seekers.models import SavedJob

from notification.models import Notification
from notification.serializers import GetNotificationSerializers
from users.models import User


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
        notification_type = self.request.GET.get('type', None)
        created = self.request.GET.get('created', None)
        exact_date = self.request.GET.get('exact_date', None)
        queryset = Notification.objects.filter(user=self.request.user)
        if created:
            queryset = queryset.filter(created__date__lte=created)
        if exact_date:
            queryset = queryset.filter(created__date=exact_date)
        if notification_type == "message":
            queryset = queryset.filter(notification_type='message')
        elif notification_type == "jobs":
            queryset = queryset.exclude(notification_type='message')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, context={"request": request})
        return response.Response(serializer.data)

    def post(self, request):
        context = dict()
        try:
            Notification.objects.filter(user=request.user).update(seen=True)
            context['notification_count'] = Notification.objects.filter(user=request.user, seen=False).count()
            context['message'] = "Notification seen successfully"
            return response.Response(
                data=context,
                status=status.HTTP_200_OK
            )
        except Notification.DoesNotExist:
            return response.Response(
                data={"notificationId": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["message"] = str(e)
            return response.Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
            )
            
    def put(self, request, notificationId):
        context = dict()
        try:
            notification_instance = Notification.objects.get(id=notificationId)
            notification_instance.seen = True
            notification_instance.save()
            
            context['notification_count'] = Notification.objects.filter(user=request.user, seen=False).count()
            context['message'] = "Notification seen successfully"
            return response.Response(
                data=context,
                status=status.HTTP_200_OK
            )
        except Notification.DoesNotExist:
            return response.Response(
                data={"notificationId": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["message"] = str(e)
            return response.Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
            )

def ExpiredSavedJobs():
    """
    Sends notifications to users who have saved job postings that have passed their deadline and have not been notified
    yet.

    Returns a HTTP response object indicating that all notifications have been sent.
    """

    saved_job_data = SavedJob.objects.filter(job__deadline__lte=date.today(), notified=False)
    if saved_job.user.get_notification:
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
            email_context["job_link"] = Common.FRONTEND_BASE_URL + "/jobs/details/" + str(saved_job.job.slug)
            if job_filter.user.get_email:
                get_email_object(
                    subject=f'Notification for expired save job',
                    email_template_name='email-templates/send-notification-old.html',
                    context=email_context,
                    to_email=[job_filter.user.email, ]
                )
        saved_job_data = SavedJob.objects.filter(
            job__deadline__lte=date.today(), notified=False
        ).update(notified=True)
    return HttpResponse("done")


class NotificationSettingsView(generics.GenericAPIView):
    """
    A view for updating the notification settings of a user.

    This view handles the PUT request for toggling the email or notification settings
    of the authenticated user. It updates the corresponding settings in the User model
    and returns a response with the updated settings and a status code.

    Attributes:
        permission_classes (list): A list of permission classes to apply to the view.

    Methods:
        put(request, notificationType): Handles the PUT request for updating the notification settings.
    
    Example usage:
        PUT /notification-settings/email
        PUT /notification-settings/notification
    """

    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, notificationType):
        """
        Handle the PUT request for updating the notification settings.

        Args:
            request (HttpRequest): The HTTP request object.
            notificationType (str): The type of notification settings to update ('email' or 'notification').

        Returns:
            Response: A response object containing the updated settings and a status code.

        Raises:
            Exception: If any error occurs during the update process.
        """
        context = dict()
        try:
            user = self.request.user
            user_instance = User.objects.get(id=request.user.id)

            if notificationType == 'email':
                if user_instance.get_email == True:
                    user_instance.get_email = False
                    context['message'] = "Mail settings are inactive"
                else:
                    user_instance.get_email = True
                    context['message'] = "Mail settings are active"

            if notificationType == 'notification':
                if user_instance.get_notification == True:
                    user_instance.get_notification = False
                    context['message'] = "Notification settings are inactive"
                else:
                    user_instance.get_notification = True
                    context['message'] = "Notification settings are active"

            user_instance.save()

            return response.Response(
                data=context,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            context["message"] = str(e)
            return response.Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
            )


class GetNotificationSettingsView(generics.GenericAPIView):
    
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        
        context = dict()
        try:
            user = self.request.user
            user_instance = User.objects.get(id=request.user.id)
            context['email'] = user_instance.get_email
            context['notification'] = user_instance.get_notification
            return response.Response(
                data=context,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            context["message"] = str(e)
            return response.Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
            )
            
