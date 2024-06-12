from django.core.handlers.wsgi import WSGIHandler
from django.core.signals import request_finished
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404
import threading
from datetime import datetime, date

from rest_framework import (
    generics, response, status,
    permissions, serializers, filters
)

from core.pagination import CustomPagination
from core.emails import get_email_object

from jobs.models import JobDetails, JobFilters
from vendors.models import AppliedTender, VendorSector
from vendors.serializers import GetAppliedTenderSerializers

from job_seekers.models import AppliedJob, Categories
from jobs.serializers import (
    GetJobsSerializers, AppliedJobSerializers
)

from notification.models import Notification

from user_profile.models import EmployerProfile
from users.models import User

from tenders.models import TenderDetails
from tenders.serializers import TendersSerializers


from superadmin.models import (
    Invoice, PointDetection, InvoiceFooter,
    SMTPSetting, RechargeHistory, InvoiceIcon
)
from superadmin.process import html_to_pdf
from koor.config.common import Common

from .models import BlackList
from .serializers import (
    UpdateAboutSerializers,
    CreateJobsSerializers,
    UpdateJobSerializers,
    CreateTendersSerializers,
    UpdateTenderSerializers,
    ActivitySerializers,
    BlacklistedUserSerializers,
    ShareCountSerializers
)


import calendar
from django.utils.html import strip_tags

def process_description(description):
    # Remove HTML tags from the description
    description = strip_tags(description)
    
    # return description
    # Check if description is greater than 30 characters
    if len(description) > 30:
        truncated_description = description[:30] + "..."  # Truncate the description
        return truncated_description
    else:
        return description


def generate_pdf_file(invoice_id):
    """
    Generate a PDF invoice file based on the provided invoice ID.

    This function retrieves relevant data from the database and generates a PDF invoice file using an HTML template.
    The generated file includes information about the invoice, user details, and recharge history.

    Parameters:
    - invoice_id (int): The ID of the invoice for which the PDF is to be generated.

    Returns:
    - file_response (bytes): A byte stream containing the generated PDF invoice file.

    Note:
    - This function requires access to the Invoice, SMTPSetting, and RechargeHistory models.
    - The HTML template used for PDF generation is 'email-templates/pdf-invoice.html'.
    - The invoice data is fetched from the Invoice model based on the provided invoice ID.
    - User's mobile number is formatted and displayed along with the country code.
    - Recharge history data is fetched for the user within the invoice date range.
    - The PDF generation is done using the 'html_to_pdf' function with the provided template
      and relevant data.

    Example usage:
    >>> invoice_id = 123
    >>> pdf_file = generate_pdf_file(invoice_id)
    >>> with open('invoice.pdf', 'wb') as file:
    ...     file.write(pdf_file)

    """
    Page_title = "KOOR INVOICE"
    invoice_month = calendar.month_name[datetime.now().month]
    invoice_data = Invoice.objects.get(invoice_id=invoice_id)
    if invoice_data.start_date:
        invoice_month = calendar.month_name[invoice_data.start_date.month]
    else:
        invoice_month = calendar.month_name[invoice_data.created.month]
    smtp_setting = SMTPSetting.objects.last()
    invoice_icons = InvoiceIcon.objects.all()
    mobile_number = invoice_data.user.mobile_number
    new_mobile_number = ""
    history_data = None
    if mobile_number:
        for i in range(0, len(mobile_number), 5):
            new_mobile_number += mobile_number[i:i + 5] + " "
        if new_mobile_number:
            new_mobile_number = invoice_data.user.country_code + " " + new_mobile_number
    if invoice_data.start_date and invoice_data.end_date and invoice_data.user:
        history_data = RechargeHistory.objects.filter(
            user=invoice_data.user, created__gte=invoice_data.start_date,
            created__lte=invoice_data.end_date
        )
    invoice_x = ""
    invoice_youtube = ""
    invoice_instagram = ""
    invoice_linkedin = ""
    invoice_facebook = ""
    invoice_link_x = ""
    invoice_link_youtube = ""
    invoice_link_instagram = ""
    invoice_link_linkedin = ""
    invoice_link_facebook = ""
    for get_invoice_data in invoice_icons:
        if get_invoice_data.type == 'x':
            invoice_x = Common.BASE_URL + get_invoice_data.icon.url
            invoice_link_x = get_invoice_data.link
        if get_invoice_data.type == 'youtube':
            invoice_youtube = Common.BASE_URL + get_invoice_data.icon.url
            invoice_link_youtube = get_invoice_data.link
        if get_invoice_data.type == 'instagram':
            invoice_instagram = Common.BASE_URL + get_invoice_data.icon.url
            invoice_link_instagram = get_invoice_data.link
        if get_invoice_data.type == 'linkedin':
            invoice_linkedin = Common.BASE_URL + get_invoice_data.icon.url
            invoice_link_linkedin = get_invoice_data.link
        if get_invoice_data.type == 'facebook':
            invoice_facebook = Common.BASE_URL + get_invoice_data.icon.url
            invoice_link_facebook = get_invoice_data.link
    invoice_footer_icon = InvoiceFooter.objects.last()
    stamp = Common.BASE_URL + invoice_footer_icon.stamp.url
    sign = Common.BASE_URL + invoice_footer_icon.signature.url
    file_response = html_to_pdf('email-templates/pdf-invoice.html', {'pagesize': 'A4', 'invoice_data': invoice_data,
                                                            'Page_title': Page_title, 'invoice_month':invoice_month,
                                                            'LOGO': Common.BASE_URL + smtp_setting.logo.url,
                                                            'stamp':stamp,
                                                            'sign':sign,
                                                            'invoice_x':invoice_x,
                                                            'invoice_youtube':invoice_youtube,
                                                            'invoice_instagram':invoice_instagram,
                                                            'invoice_linkedin':invoice_linkedin,
                                                            'invoice_facebook':invoice_facebook,
                                                            'invoice_link_x':invoice_link_x,
                                                            'invoice_link_youtube':invoice_link_youtube,
                                                            'invoice_link_instagram':invoice_link_instagram,
                                                            'invoice_link_linkedin':invoice_link_linkedin,
                                                            'invoice_link_facebook':invoice_link_facebook,
                                                            'mobile_number':new_mobile_number,
                                                            'history_data':history_data
                                                        }, raw=True
                    )
    return file_response


def generate_merge_pdf_file(invoice_list, employer_data):
    invoices = Invoice.objects.filter(invoice_id__in=invoice_list).filter(user=employer_data).order_by('created')
    Page_title = "KOOR INVOICE"
    last_invoice = invoices.last()
    invoice_month = calendar.month_name[datetime.now().month]
    invoice_date = datetime.now().date
    amount = 0.0
    discount = 0.0
    grand_total = 0.0
    for get_invoices in invoices:
        amount = amount + float(get_invoices.total)
        
    # discount = amount
    grand_total = amount - discount
    smtp_setting = SMTPSetting.objects.last()
    invoice_icons = InvoiceIcon.objects.all()
    mobile_number = last_invoice.user.mobile_number
    new_mobile_number = ""
    history_data = None
    if mobile_number:
        for i in range(0, len(mobile_number), 5):
            new_mobile_number += mobile_number[i:i + 5] + " "
        if new_mobile_number:
            new_mobile_number = last_invoice.user.country_code + " " + new_mobile_number
    
    invoice_x = ""
    invoice_youtube = ""
    invoice_instagram = ""
    invoice_linkedin = ""
    invoice_facebook = ""
    invoice_link_x = ""
    invoice_link_youtube = ""
    invoice_link_instagram = ""
    invoice_link_linkedin = ""
    invoice_link_facebook = ""
    for invoice_data in invoice_icons:
        if invoice_data.type == 'x':
            invoice_x = Common.BASE_URL + invoice_data.icon.url
            invoice_link_x = invoice_data.link
        if invoice_data.type == 'youtube':
            invoice_youtube = Common.BASE_URL + invoice_data.icon.url
            invoice_link_youtube = invoice_data.link
        if invoice_data.type == 'instagram':
            invoice_instagram = Common.BASE_URL + invoice_data.icon.url
            invoice_link_instagram = invoice_data.link
        if invoice_data.type == 'linkedin':
            invoice_linkedin = Common.BASE_URL + invoice_data.icon.url
            invoice_link_linkedin = invoice_data.link
        if invoice_data.type == 'facebook':
            invoice_facebook = Common.BASE_URL + invoice_data.icon.url
            invoice_link_facebook = invoice_data.link
    invoice_footer_icon = InvoiceFooter.objects.last()
    stamp = Common.BASE_URL + invoice_footer_icon.stamp.url
    sign = Common.BASE_URL + invoice_footer_icon.signature.url
    file_response = html_to_pdf('email-templates/merge-pdf-invoice.html', {'pagesize': 'A4', 'invoice_data': invoices,
                                                            'Page_title': Page_title, 'invoice_month':invoice_month,
                                                            'LOGO': Common.BASE_URL + smtp_setting.logo.url,
                                                            'invoice_x':invoice_x,
                                                            'stamp':stamp,
                                                            'sign':sign,
                                                            'invoice_youtube':invoice_youtube,
                                                            'invoice_instagram':invoice_instagram,
                                                            'invoice_linkedin':invoice_linkedin,
                                                            'invoice_facebook':invoice_facebook,
                                                            'invoice_link_x':invoice_link_x,
                                                            'invoice_link_youtube':invoice_link_youtube,
                                                            'invoice_link_instagram':invoice_link_instagram,
                                                            'invoice_link_linkedin':invoice_link_linkedin,
                                                            'invoice_link_facebook':invoice_link_facebook,
                                                            'mobile_number':new_mobile_number,'last_invoice':last_invoice,
                                                            'history_data':history_data, 'invoice_date':invoice_date,
                                                            'amount':amount, 'discount':discount, 'grand_total':grand_total,
                                                        }, raw=True
                    )
    return file_response



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
        elif self.request.user.role == "admin":
            user_id = request.GET.get('userId', None)
            if user_id:
                user_instance = User.objects.get(id=user_id)
                profile_instance = get_object_or_404(EmployerProfile, user=user_instance)
            else:
                context['message'] = "userId is required for update employer profile."
                return response.Response(
                    data=context,
                    status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
            )        
        serializer = self.serializer_class(data=request.data, instance=profile_instance, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            if 'email' in serializer.validated_data:
                if User.objects.filter(email__iexact=serializer.validated_data['email']).exists():
                    if profile_instance.user.email.lower() != serializer.validated_data['email'].lower():
                        context['email'] = ["email already in use."]
                        return response.Response(
                            data=context,
                            status=status.HTTP_400_BAD_REQUEST
                        )
            if 'mobile_number' in serializer.validated_data:
                if User.objects.filter(mobile_number=serializer.validated_data['mobile_number']).exists():
                    if profile_instance.user.mobile_number != serializer.validated_data['mobile_number']:
                        context['mobile_number'] = ["mobile number already in use."]
                        return response.Response(
                            data=context,
                            status=status.HTTP_400_BAD_REQUEST
                        )
            if serializer.update(profile_instance, serializer.validated_data):
                if self.request.user.role == "admin":
                    profile_instance.user.email = request.data['email']
                    profile_instance.user.save()
                    
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
    search_fields = [
        'title', 'description',
        'skill__title', 'highest_education__title',
        'job_category__title', 'job_sub_category__title',
        'country__title', 'city__title'
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
        context = {}
        email_context = {}
        serializer = CreateJobsSerializers(data=request.data)
        employer_profile_instance = get_object_or_404(EmployerProfile, user=request.user)
        point_data = PointDetection.objects.first()

        if request.user.role == "employer" and employer_profile_instance.is_verified:
            serializer.is_valid(raise_exception=True)
            if employer_profile_instance.points < point_data.points:
                context["message"] = "You do not have enough points to create a new job."
                return response.Response(data=context, status=status.HTTP_400_BAD_REQUEST)

            job_instance = serializer.save(request.user)
            remaining_points = employer_profile_instance.points - point_data.points
            employer_profile_instance.points = remaining_points
            employer_profile_instance.save()
                        
            total = float(point_data.points)
            discount = float(point_data.points)
            grand_total = float(point_data.points) - discount

            invoice_instance = Invoice.objects.create(
                user=request.user, job=job_instance, points=point_data.points,
                total=total, discount=discount, grand_total=grand_total
            )
            email_context["yourname"] = employer_profile_instance.user.name
            email_context["type"] = 'job'
            email_context['Ctype'] = 'Job'
            email_context["title"] = request.data['title']
            email_context["job_id"] = job_instance.job_id
            email_context["job_instance"] = job_instance
            email_context["job_link"] = Common.FRONTEND_BASE_URL + "/jobs/details/" + str(job_instance.slug)
            email_context["discription"] = process_description(job_instance.description)
            
            if employer_profile_instance.user.email:
                get_email_object(
                    subject=f'Koor Published: ' + str(request.data['title']),
                    email_template_name='email-templates/create-jobs.html',
                    context=email_context,
                    to_email=[employer_profile_instance.user.email, ]
                )
        
                pdf = generate_pdf_file(invoice_instance.invoice_id)
                get_email_object(
                    subject=f'Mail for Invoice',
                    email_template_name='email-templates/mail-for-invoice.html',
                    context=email_context,
                    to_email=[employer_profile_instance.user.email, ],
                    type="attachment",
                    filename="Invoice.pdf", 
                    file=pdf
                )

            context["message"] = "Job added successfully."
            context["remaining_points"] = remaining_points
            # Create a new thread for the background task
            background_thread = threading.Thread(target=my_callback)

            # Start the background thread
            background_thread.start()
            
            return response.Response(data=context, status=status.HTTP_201_CREATED)
        else:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(data=context, status=status.HTTP_401_UNAUTHORIZED)

        return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


def my_callback():
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
        Q(job_sub_category__in=[(job_sub_category_value) for job_sub_category_value in
                                job_instance.job_sub_category.all()]) | Q(
            job_sub_category=None)
    ).filter(
        Q(is_full_time=job_instance.is_full_time) | Q(is_full_time=None)
    ).filter(
        Q(is_part_time=job_instance.is_part_time) | Q(is_part_time=None)
    ).filter(
        Q(has_contract=job_instance.has_contract) | Q(has_contract=None)
    ).filter(
        Q(duration=job_instance.duration) | Q(duration=None)
    )
    
    if job_instance.job_sub_category.all():
        users = Categories.objects.filter(category__in=job_instance.job_sub_category.all()).values_list('user', flat=True).order_by('user').distinct('user')
    else:
        users = Categories.objects.filter(category__category__in=job_instance.job_category.all()).values_list('user', flat=True).order_by('user').distinct('user')
    for get_user_data in users:
        user_instance = User.objects.get(id=get_user_data)
        if user_instance.get_notification:
            Notification.objects.bulk_create(
                [
                    Notification(
                        user=user_instance,
                        job=job_instance,
                        notification_type='job_preference',
                        created_by=job_instance.user
                    )
                ]
            )
        if user_instance.email:
            context = dict()
            if user_instance.name:
                user_name = user_instance.name
            else:
                user_name = user_instance.email
            context["yourname"] = user_name
            context["notification_type"] = "job"
            context["job_instance"] = job_instance
            context["job_link"] = Common.FRONTEND_BASE_URL + "/jobs/details/" + str(job_instance.slug)
            if user_instance.get_email:
                get_email_object(
                    subject=f'New job alert - ' + str(job_instance.title),
                    email_template_name='email-templates/send-notification.html',
                    context=context,
                    to_email=[user_instance.email, ]
                )
        
    
    for job_filter in job_filter_data:
        if job_filter.user.get_notification:
            Notification.objects.bulk_create(
                [
                    Notification(
                        user=job_filter.user,
                        job_filter=job_filter,
                        job=job_instance,
                        notification_type='advance_filter',
                        created_by=job_instance.user
                    )
                ]
            )
        for job_filter in job_filter_data:
            if job_filter.user.email:
                context = dict()
                if job_filter.user.name:
                    user_name = job_filter.user.name
                else:
                    user_name = job_filter.user.email
                context["yourname"] = user_name
                context["notification_type"] = "job"
                context["job_instance"] = job_instance
                context["job_link"] = Common.FRONTEND_BASE_URL + "/jobs/details/" + str(job_instance.slug)
                if job_filter.user.get_email:
                    get_email_object(
                        subject=f'New job alert - ' + str(job_instance.title),
                        email_template_name='email-templates/send-notification.html',
                        context=context,
                        to_email=[job_filter.user.email, ]
                    )
    
    
    # request_finished.disconnect(my_callback, sender=WSGIHandler, dispatch_uid='notification_trigger_callback')


class TendersView(generics.ListAPIView):
    """
    A class-based view for retrieving a list of tenders filtered and paginated according to search criteria.

    Serializer class used: TendersSerializers
    Permission class used: permissions.IsAuthenticated
    Filter backend used: filters.SearchFilter
    Search fields used:
        - 'title': title of the tender
        - 'description': description of the tender
        - 'tag__title': tag title associated with the tender
        - 'tender_type': type of the tender
        - 'sector': sector associated with the tender
        - 'tender_category__title': tender category title associated with the tender
        - 'country__title': country title associated with the tender
        - 'city__title': city title associated with the tender

    Pagination class used: CustomPagination

    Attributes:
        - serializer_class (TendersSerializers): The serializer class used to serialize the tenders
        - permission_classes (list): The permission classes required for accessing the view
        - queryset (None): The initial queryset used to retrieve the tenders. It is set to None and will be overridden.
        - filter_backends (list): The filter backends used for filtering the tenders
        - search_fields (list): The search fields used for searching the tenders
        - pagination_class (CustomPagination): The pagination class used for pagination of the tenders
    """

    serializer_class = TendersSerializers
    permission_classes = [permissions.IsAuthenticated]
    queryset = None
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'title', 'description',
        'tag__title', 'tender_type__title', 'sector__title',
        'tender_category__title', 'country__title',
        'city__title'
    ]
    pagination_class = CustomPagination

    def list(self, request):
        """
        A method that handles the HTTP GET request for retrieving a list of resources, with the condition that the user
        role is an employer.

        Args:
            - `request (HttpRequest)`: The HTTP request object.

        Returns:
            - A JSON response containing a list of serialized resources or an error message with an HTTP status code.

        Raises:
            N/A

        Behaviour:
            - If the user role is 'employer', the queryset is filtered and paginated before being serialized using the
                `get_serializer` method, with the current user's details being passed into the context. The serialized
                    data is then returned in a paginated response if paginated, or just the serialized data if not.
            - If the user role is not 'employer', a message indicating the user's lack of permission is returned with
                an HTTP status code of 401 (unauthorized).

        Attributes:
            N/A
        """

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

    def get_queryset(self, **kwargs):
        """
        A method that returns a queryset of `TenderDetails instances`. It filters the queryset based on the
        `employer ID` provided in the `request query parameters`.
        If the `'employerId'` parameter is provided, it filters the queryset to include only the TenderDetails
        instances associated with the specified `user ID`. Otherwise, it returns `all TenderDetails` instances.

        Args:
            **kwargs: A dictionary of keyword arguments.

        Returns:
            QuerySet: A filtered queryset of TenderDetails instances.

        """

        user_id = self.request.GET.get('employerId', None)
        if not user_id:
            user_id = self.request.user.id
        user_data = User.objects.get(id=user_id)
        return TenderDetails.objects.filter(user=user_data).order_by('-created')

    def post(self, request):
        """
        Handles POST requests to create a new `TenderDetails` instance.

        Args:
            - `request`: The HTTP request object.

        Returns:
            - A response object with the following possible status codes:
                - `HTTP_201_CREATED`: The tender was created successfully.
                - `HTTP_400_BAD_REQUEST`: The request data was invalid or there was an error saving the tender.
                - `HTTP_401_UNAUTHORIZED`: The user does not have permission to create a tender.

        """

        context = dict()
        email_context = dict()
        serializer = CreateTendersSerializers(data=request.data)
        try:
            employer_profile_instance = get_object_or_404(EmployerProfile, user=self.request.user)
            point_data = PointDetection.objects.first()
            if self.request.user.role == "employer" and employer_profile_instance.is_verified:
                serializer.is_valid(raise_exception=True)
                if employer_profile_instance.points < point_data.points:
                    context["message"] = "You do not have enough points to create a new job."
                    return response.Response(data=context, status=status.HTTP_400_BAD_REQUEST)
                
                tender_instance = serializer.save(self.request.user)
                remaining_points = employer_profile_instance.points - point_data.points
                employer_profile_instance.points = remaining_points
                employer_profile_instance.save()
                            
                total = float(point_data.points)
                discount = float(point_data.points)
                grand_total = float(point_data.points) - discount
                
                invoice_instance = Invoice.objects.create(
                    user=request.user, tender=tender_instance, points=point_data.points,
                    total=total, discount=discount, grand_total=grand_total
                )               
                
                email_context["yourname"] = self.request.user.name
                email_context["type"] = 'tender'
                email_context["title"] = request.data['title']
                email_context['Ctype'] = 'Tender'
                email_context["job_id"] = tender_instance.tender_id
                email_context["job_instance"] = tender_instance
                
                email_context["job_link"] = Common.FRONTEND_BASE_URL + "/tender/details/" + str(tender_instance.slug)
                email_context["discription"] = process_description(tender_instance.description)
                if self.request.user.email:
                    get_email_object(
                        subject=f'Koor Published: '+ str(request.data['title']),
                        email_template_name='email-templates/create-jobs.html',
                        context=email_context,
                        to_email=[self.request.user.email, ]
                    )
                    
                    pdf = generate_pdf_file(invoice_instance.invoice_id)
                    get_email_object(
                        subject=f'Mail for Invoice',
                        email_template_name='email-templates/mail-for-invoice.html',
                        context=email_context,
                        to_email=[employer_profile_instance.user.email, ],
                        type="attachment",
                        filename="Invoice.pdf", 
                        file=pdf
                    )
                
                context["message"] = "Tender added successfully."
                # Create a new thread for the background task
                background_thread = threading.Thread(target=tender_callback)

                # Start the background thread
                background_thread.start()
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

    def put(self, request, tendersId):
        """
        Update an existing tender instance with the provided request data.

        Args:
            - `request`: An instance of the Django Request object.

        Returns:
            An instance of the Django Response object with a JSON-encoded message indicating whether the tender instance
            was updated successfully or not.

        Raises:
            - `Http404`: If the TenderDetails instance with the provided tendersId does not exist.

        Notes:
            This method requires a tendersId to be included in the request data, and will only update the tender if the
            authenticated user matches the user associated with the tender instance. The UpdateTenderSerializers class
            is used to serialize the request data and update the tender instance. If the serializer is invalid or the
            user does not have permission to update the tender instance, an appropriate error response is returned.
        """
        context = dict()
        try:
            tender_instance = TenderDetails.objects.get(id=tendersId)
            if request.user == tender_instance.user:
                serializer = UpdateTenderSerializers(data=request.data, instance=tender_instance, partial=True)
                try:
                    serializer.is_valid(raise_exception=True)
                    if serializer.update(tender_instance, serializer.validated_data):
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
        except TenderDetails.DoesNotExist:
            return response.Response(
                data={"tendersId": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["message"] = str(e)
            return response.Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
            )


def tender_callback():
    
    tender_instance = TenderDetails.objects.first()
    sectors = tender_instance.sector.all()
    # Initialize an empty list to store filtered VendorSector objects
    tender_filter_data = []

    # Iterate over each sector and filter VendorSector objects
    for sector in sectors:
        filtered_data = VendorSector.objects.filter(sector=sector)
        tender_filter_data.extend(filtered_data)
        
    print(tender_filter_data, 'jojoj')
    for tender_filter in tender_filter_data:
        if tender_filter.user.email:
            context = dict()
            if tender_filter.user.name:
                user_name = tender_filter.user.name
            else:
                user_name = tender_filter.user.email
            context["yourname"] = user_name
            context["notification_type"] = "tender"
            context["job_instance"] = tender_instance
            context["job_link"] = Common.FRONTEND_BASE_URL + "/tender/details/" + str(tender_instance.slug)
            if tender_filter.user.get_email:
                get_email_object(
                    subject=f'New tender alert - ' + str(tender_instance.title),
                    email_template_name='email-templates/send-notification.html',
                    context=context,
                    to_email=[tender_filter.user.email, ]
                )



class JobsStatusView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, jobId):
        """
        View function for `updating the status` of a job instance.

        Args:
            - `request`: Request object containing metadata about the current request.
            - `jobId`: Integer representing the ID of the job instance to be updated.

        Returns:
            Response object containing data about the updated job instance, along with an HTTP status code.

        Raises:
            - `Http404`: If the job instance with the given `jobId does not exist`.
        """

        context = dict()
        try:
            jobs_instance = JobDetails.objects.get(id=jobId)
            if request.user == jobs_instance.user:
                if jobs_instance.status == "hold":
                    jobs_instance.status = "active"
                    context['message'] = "This job is active"
                elif jobs_instance.status == "active":
                    jobs_instance.status = "hold"
                    context['message'] = "This job placed on hold"
                jobs_instance.save()
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            else:
                context['message'] = "You do not have permission to perform this action."
                return response.Response(
                    data=context,
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except JobDetails.DoesNotExist:
            return response.Response(
                data={"jobId": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["message"] = e
            return response.Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
            )


class TendersStatusView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, tendersId):
        """
        View function for `updating the status` of a tenders instance.

        Args:
            - `request`: Request object containing metadata about the current request.
            - `tendersId`: Integer representing the ID of the tenders instance to be updated.

        Returns:
            Response object containing data about the updated tenders instance, along with an HTTP status code.

        Raises:
            - `Http404`: If the tenders instance with the given `tendersId does not exist`.
        """

        context = dict()
        try:
            tenders_instance = TenderDetails.objects.get(id=tendersId)
            if request.user == tenders_instance.user:
                if tenders_instance.status == "hold":
                    tenders_instance.status = "active"
                    context['message'] = "This tender is active"
                elif tenders_instance.status == "active":
                    tenders_instance.status = "hold"
                    context['message'] = "This tender placed on hold"
                tenders_instance.save()
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            else:
                context['message'] = "You do not have permission to perform this action."
                return response.Response(
                    data=context,
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except TenderDetails.DoesNotExist:
            return response.Response(
                data={"tendersId": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["message"] = e
            return response.Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
            )


class ActivityView(generics.GenericAPIView):
    """
    View for retrieving various activity-related information for a user.

    This view requires the user to be authenticated and returns information on active jobs and tenders that a user has,
    as well as jobs and tenders that the user has applied for.

    Attributes:
        - `permission_classes`: A list of permission classes that the view requires.
        - `serializer_class`: The serializer class to be used for this view.

    Methods:
        - `get`: Handles GET requests and retrieves activity-related information for the user.

    Usage:
        To use this view, make a GET request to the view's endpoint. For example:

            GET `/activity/`

        The request must include a valid authentication token in the Authorization header.
        If the user is an employer, the view will return activity-related information for that employer. If the user
        is not an employer, the view will return an error message.

    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ActivitySerializers

    def get(self, request):
        """
        Retrieves activity-related information for the user.

        If the user is an employer, returns information on active jobs and tenders that the user has, as well as jobs
        and tenders that the user has applied for. If the user is not an employer, returns an error message.

        Returns:
            A Response object containing the serialized activity-related information or an error message.
        """

        context = dict()
        if self.request.user.role == "employer":
            try:
                serializer = self.get_serializer(request.user)
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
        else:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
            )


class JobAnalysisView(generics.GenericAPIView):
    """
    A view that returns month-wise count of job details created by employers.

    permission_classes:
        - `IsAuthenticated`: User must be authenticated.

    HTTP Methods:
        - `GET`: Get the count of job details created by employers per month.

    Returns:
        - `200 OK`: Returns a JSON object with the `month-wise count` of job details.
        - `400 BAD REQUEST`: Returns a JSON object with an error message if an exception occurs.
        - `401 UNAUTHORIZED`: Returns a JSON object with an error message if the user is not an employer.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Get the count of job details created by employers per month.

            - If the user is an employer, returns a JSON object with the month-wise count of job details.
            - If the user is not an employer, returns a JSON object with an error message.
            - If an exception occurs, returns a JSON object with an error message.

        Returns:
            - A JSON object with the month-wise count of job details or an error message.
        """

        context = dict()
        if self.request.user.role == "employer":
            try:
                order_counts = JobDetails.objects.filter(user=self.request.user).annotate(
                    month=TruncMonth('created')
                ).values('month').annotate(count=Count('id'))
                data = {'order_counts': list(order_counts)}
                return response.Response(
                    data=data,
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                context['message'] = str(e)
                return response.Response(
                    data=context,
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
            )


class BlacklistedUserView(generics.ListAPIView):
    """
    View for retrieving a list of `BlackListedUser` objects.

    This view is used to retrieve a list of `BlackListedUser` objects in a paginated format. The view requires the user
    to be authenticated and have the role of '`employer`'. The view returns a serialized representation of the queryset
    in JSON format.

    Attributes:
        - `serializer_class (class)`: The serializer class to be used for serializing the queryset, which is the
            `BlacklistedUserSerializers` class.
        - `permission_classes (list)`: A list of permission classes to be used for checking the user's permissions,
            which includes only the `IsAuthenticated` permission class.
        - `queryset (QuerySet)`: The queryset to be used for retrieving the `BlackListedUser` objects, which includes
            all objects in the `BlackList` model.
        - `pagination_class (class)`: The pagination class to be used for paginating the queryset, which is the
            `CustomPagination` class.

    Methods:
        - `list(self, request)`: The method used to handle `GET` requests to retrieve the list of `BlackListedUser`
            objects. If the user has the role of '`employer`', the method filters the queryset to include only the
            `BlackListedUser` objects where the user is the current user and paginates the filtered queryset. If the
            user does not have the role of '`employer`', the method returns an error message with a `401 unauthorized`
            status.

    """

    serializer_class = BlacklistedUserSerializers
    permission_classes = [permissions.IsAuthenticated]
    queryset = BlackList.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'blacklisted_user__email', 'blacklisted_user__name',
        'blacklisted_user__role', 'blacklisted_user__mobile_number'
    ]
    pagination_class = CustomPagination

    def list(self, request):
        context = dict()
        if self.request.user.role == 'employer':
            queryset = self.filter_queryset(self.get_queryset().filter(user=request.user))
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return response.Response(serializer.data)
        else:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
            )


class ShareCountView(generics.GenericAPIView):
    """
    The ShareCountView is a class-based view that returns the number of shares made by the authenticated user.

    Attributes:
        - `permission_classes (list)`: A list of permission classes that must be satisfied in order for the view to be
            accessed. In this case, only authenticated users can access the view.
        - `serializer_class (class)`: The serializer class that will be used to serialize and deserialize the data
            returned by the view.

    Methods:
        - `get(self, request)`: Returns the number of shares made by the authenticated user. If the user is an
            employer, the view will attempt to serialize the user data using the serializer class specified in
            the serializer_class attribute and return the serialized data in the response. If the serialization
            fails, a 400 bad request response will be returned with an error message. If the user is not an employer,
            a 401 unauthorized response will be returned with a message indicating that the user does not have
            permission to perform the action.

    Usage:
        Instantiate ShareCountView in urls.py to map the view to a URL and provide the required authentication
        credentials for the user.

    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ShareCountSerializers

    def get(self, request):

        context = dict()
        if self.request.user.role == "employer":
            try:
                serializer = self.get_serializer(request.user)
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
        else:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
            )


class ActiveJobsView(generics.ListAPIView):
    """
    View to retrieve a list of active jobs posted by a specific employer.

    Methods:
    list(request, employerId):
        Returns a paginated list of jobs posted by the employer with the given `employerId`.

    Attributes:
    serializer_class: `GetJobsSerializers` Serializer class to use for converting queryset to JSON.
    permission_classes: `list of permissions` List of permission classes to apply to the view.
    queryset: `QuerySet` QuerySet representing all jobs in the database.
    filter_backends: `list of filter backends` List of filter backends to apply to the view.
    search_fields: `list of str` List of fields to search for in the filter_backends.
    pagination_class: `CustomPagination` Pagination class to use for paginating the queryset.
    """

    serializer_class = GetJobsSerializers
    permission_classes = [permissions.AllowAny]
    queryset = JobDetails.objects.filter(status='active')
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'title', 'description',
        'skill__title', 'highest_education__title',
        'job_category__title', 'job_sub_category__title',
        'country__title', 'city__title'
    ]
    pagination_class = CustomPagination

    def list(self, request, employerId):
        context = dict()
        user_instance = User.objects.get(id=employerId)
        queryset = self.filter_queryset(self.get_queryset().filter(user=user_instance))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"user": user_instance})
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, context={"user": user_instance})
        return response.Response(serializer.data)


class ActiveTendersView(generics.ListAPIView):

    serializer_class = TendersSerializers
    permission_classes = [permissions.AllowAny]
    queryset = TenderDetails.objects.filter(status='active')
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'title', 'description',
        'tag__title', 'tender_type__title', 'sector__title',
        'tender_category__title', 'country__title',
        'city__title'
    ]
    pagination_class = CustomPagination

    def list(self, request, employerId):
        context = dict()
        user_instance = User.objects.get(id=employerId)
        queryset = self.filter_queryset(self.get_queryset().filter(user=user_instance))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"user": user_instance})
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, context={"user": user_instance})
        return response.Response(serializer.data)


class UnblockUserView(generics.GenericAPIView):
    
    serializer_class = UpdateAboutSerializers
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, userId):
        
        context = dict()
        if request.user.role == "employer":
            try:
                user_instance = User.objects.get(id=userId)
                try:
                    blacklisted_instance = BlackList.objects.get(blacklisted_user=user_instance, user=request.user)
                    blacklisted_instance.delete(soft=False)
                    context['message'] = "User unblocked."
                    return response.Response(
                        data=context,
                        status=status.HTTP_200_OK
                    )
                except BlackList.DoesNotExist:
                    return response.Response(
                        data={"message": ["This user not block by you."]},
                        status=status.HTTP_404_NOT_FOUND
                    )
            except BlackList.DoesNotExist:
                return response.Response(
                    data={"message": ["Invalid user id."]},
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


class JobApplicationView(generics.ListAPIView):

    serializer_class = AppliedJobSerializers
    permission_classes = [permissions.IsAuthenticated]
    queryset = AppliedJob.objects.filter(job__deadline__gte=date.today()).order_by('-created')
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    pagination_class = CustomPagination

    def list(self, request, jobSeekerId):
        context = dict()
        if self.request.user.role == 'employer':
            user_instance = User.objects.get(id=jobSeekerId)
            queryset = self.filter_queryset(self.get_queryset().filter(user=user_instance).filter(job__user=self.request.user))
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True, context={"user": self.request.user})
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True, context={"user": self.request.user})
            return response.Response(serializer.data)
        else:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
            )

class TenderApplicationView(generics.ListAPIView):

    serializer_class = GetAppliedTenderSerializers
    permission_classes = [permissions.IsAuthenticated]
    queryset = AppliedTender.objects.filter(tender__deadline__gte=date.today()).order_by('-created')
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    pagination_class = CustomPagination

    def list(self, request, vendorId):
        context = dict()
        if self.request.user.role == 'employer':
            user_instance = User.objects.get(id=vendorId)
            queryset = self.filter_queryset(self.get_queryset().filter(user=user_instance).filter(tender__user=self.request.user))
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True, context={"request": request})
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True, context={"request": request})
            return response.Response(serializer.data)
        else:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
            )
            
