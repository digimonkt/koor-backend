from django.db.models import Value, F, Case, When, IntegerField, Q
from datetime import date, datetime

from django_filters import rest_framework as django_filters

from rest_framework import (
    status, generics, serializers,
    response, permissions, filters
)

from core.emails import get_email_object
from core.pagination import CustomPagination

from tenders.models import TenderDetails, TenderFilter
from tenders.filters import TenderDetailsFilter
from tenders.serializers import (
    TendersSerializers, TendersDetailSerializers,
    TenderFiltersSerializers, AppliedTenderSerializers,
    GetTenderFilterSerializers,
    TendersSuggestionSerializers,
)

from vendors.serializers import GetAppliedTenderApplicationSerializers
from vendors.models import AppliedTender

from notification.models import Notification
from employers.models import BlackList


class TenderSearchView(generics.ListAPIView):
    """
    `TenderSearchView` is a class-based view that retrieves a list of tenders from the database based on the search
    query parameters.

    Attributes:
        - `serializer_class`: The serializer class used to convert the retrieved data into a Python object.
        - `permission_classes`: The permission classes that apply to this view.
        - `queryset`: The database query to retrieve tenders with deadlines greater than or equal to today's date.
        - `filter_backends`: The filter backends to apply to the queryset.
        - `filterset_class`: The filterset class that contains the filter fields for the queryset.
        - `search_fields`: The fields that can be searched using the `search` query parameter.
        - `pagination_class`: The pagination class used to paginate the retrieved data.

    Methods:
        - `get_queryset`: Retrieves the queryset to be used in the view.

    """

    serializer_class = TendersSerializers
    permission_classes = [permissions.AllowAny]
    queryset = TenderDetails.objects.filter(deadline__gte=date.today(), status='active')
    filter_backends = [filters.SearchFilter, django_filters.DjangoFilterBackend]
    filterset_class = TenderDetailsFilter
    search_fields = [
        'title', 'description',
        'tag__title', 'tender_type__title', 'sector__title',
        'tender_category__title', 'country__title',
        'city__title'
    ]
    pagination_class = CustomPagination

    def list(self, request):
        """
        list is a method of a class-based view that returns a paginated list of tenders based on the query parameters.

        Args:
            - `request`: The request object that contains the query parameters.

        Returns:
            - Returns a paginated list of tenders based on the query parameters.

        Methods:
            - `get_queryset`: Retrieves the queryset to be used in the view.

        """

        context = dict()
        if request.user.is_authenticated:
            context = {"user": request.user}

        queryset = self.filter_queryset(self.get_queryset())
        tenderCategory = request.GET.getlist('tenderCategory')
        tag = request.GET.getlist('tag')
        sector = request.GET.getlist('sector')
        tender_type = request.GET.getlist('opportunityType')
        if tenderCategory:
            queryset = queryset.filter(tender_category__title__in=tenderCategory).distinct()
        if tag:
            queryset = queryset.filter(tag__title__in=tag).distinct()
        if sector:
            queryset = queryset.filter(sector__title__in=sector).distinct()
        if tender_type:
            queryset = queryset.filter(tender_type__title__in=tender_type).distinct()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context=context)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, context=context)
        return response.Response(serializer.data)


class TenderDetailView(generics.GenericAPIView):
    """
    A view that returns a serialized `TenderDetails` object for a given `tenderId`.

    Parameters:
        - `tenderId (int)`: The ID of the tender to retrieve details for.

    Returns:
        - `data (dict)`: A dictionary containing the serialized tender details.
        - `status (int)`: The HTTP status code of the response.
    """

    serializer_class = TendersDetailSerializers
    permission_classes = [permissions.AllowAny]

    def get(self, request, tenderId):
        """
        A Django view function that retrieves the details of a tender with a given `tenderId` using the `TenderDetails`
        model and returns the data serialized using the serializer_class.

        Parameters:
            - `request (HttpRequest)`: The HTTP request object.
            - `tenderId (int)`: The id of the tender to retrieve.

        Returns:
            - A Response object with data containing the serialized tender details and status 200 if successful.
            - A Response object with data containing an error message and status 400 if an exception occurs during the
                retrieval.

        """

        response_context = dict()
        context = dict()
        try:
            if request.user.is_authenticated:
                context = {"user": request.user}
            if tenderId:
                tender_data = TenderDetails.objects.get(id=tenderId)
                get_data = self.serializer_class(tender_data, context=context)
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


class TenderFilterView(generics.GenericAPIView):
    """
    API view for filtering tenders.

    - `Serializer`: TenderFiltersSerializers
    - `Permissions`: IsAuthenticated

    Attributes:
        - `serializer_class (TenderFiltersSerializers)`: The serializer class used to serialize and validate the
            request data.
        - `permission_classes (list)`: The list of permission classes that the user must have to access this API.
    """

    serializer_class = TenderFiltersSerializers
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Create a new object using the POST method.

        Args:
            - `request (HttpRequest)`: The request object containing the data to be serialized.

        Returns:
            - A Response object with the serialized data and an HTTP status code.

        Raises:
            - `ValidationError`: If the serializer's validation fails.

        """

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
        get is a method of the `TenderFilterView` class that handles HTTP GET requests to retrieve TenderFilter objects
        saved by a particular user.

        Args:
            - `request (HttpRequest)`: An HTTP GET request.

        Returns:
            - `HttpResponse`: A JSON response containing a serialized list of TenderFilter objects associated with the
                authenticated user who made the request and a status code of 200 OK, or a JSON error response with a
                status code of 400 BAD REQUEST.

        Raises:
            - `Exception`: If there is an error retrieving the TenderFilter objects.

        Usage:
            - This method is used to handle GET requests made to the TenderFilterView view. It first creates a context
                dictionary to store any additional data to be passed to the serializer.
            - It then retrieves all TenderFilter objects associated with the authenticated user who made the request
                using the filter method.
            - The data is serialized using the GetTenderFilterSerializers class and returned as a JSON response with a
                status code of 200 OK.
            - If there is an error retrieving the data, a JSON error response is returned with a status code of 400
                BAD REQUEST.
        """

        context = dict()
        try:
            tender_filter_data = TenderFilter.objects.filter(user=request.user)
            get_data = GetTenderFilterSerializers(tender_filter_data, many=True)
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

    def put(self, request, filterId):
        """
        Updates the `TenderFilter` instance corresponding to the given filterId and authenticated user with the provided
        data in the request.

        Args:
            - `request (HttpRequest)`: The HTTP request object.
            - `filterId (int)`: The id of the `TenderFilter` instance to be updated.

        Returns:
            - A Response object with status code and message indicating the success or failure of the operation.
            - Successful response has status code 200 and a message "`Updated Successfully`".
            - In case of invalid serializer data, returns a Response object with status code 400 and serializer errors.
            - In case the TenderFilter instance with the given `filterId` does not exist for the authenticated user,
            returns a Response object with status code 404 and `{"filterId": "Does Not Exist"}`.
            - In case of any other exception, returns a Response object with status code 404 and the exception message.
        """

        context = dict()
        try:
            filter_instance = TenderFilter.all_objects.get(id=filterId, user=request.user)
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
        except TenderFilter.DoesNotExist:
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

    def delete(self, request, filterId):
        """
        A function to delete a tender filter instance.

        Args:
        - `request (HttpRequest)`: An HTTP request object.
        - `filterId (int)`: An integer representing the ID of the tender filter instance to be deleted.

        Returns:
        - A Response object with a JSON representation of a message indicating the result of the operation and the HTTP
            status code.

        Raises:
        - `TenderFilter.DoesNotExist`: If the tender filter instance with the given filterId and user does not exist.
        - `Exception`: If there is any other error during the deletion process.
        """

        context = dict()
        try:
            TenderFilter.all_objects.get(id=filterId, user=request.user).delete(soft=False)
            context['message'] = "Filter Removed"
            return response.Response(
                data=context,
                status=status.HTTP_200_OK
            )
        except TenderFilter.DoesNotExist:
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


class TenderSuggestionView(generics.ListAPIView):
    """
    API view for suggesting tenders based on matching criteria.

    This view provides a list of suggested tenders based on matching criteria, including the budget amount, tags,
    tender category, tender type, and sector.

    Attributes:
        - serializer_class (class): The serializer class for the TenderDetails model.
        - permission_classes (list): A list of permission classes to determine access to the view.
        - queryset (QuerySet): The initial queryset for retrieving TenderDetails objects.
        - filter_backends (list): A list of filter backends to apply for filtering the queryset.
        - filterset_class (class): The filter class to use for filtering the queryset.
        - search_fields (list): A list of fields to search for matching keywords.
        - pagination_class (class): The pagination class for paginating the results.

    Methods:
        list(request, tenderId): Retrieves the suggested tenders based on the given tenderId.

    Raises:
        TenderDetails.DoesNotExist: If the specified tenderId does not exist.
    """

    serializer_class = TendersSuggestionSerializers
    permission_classes = [permissions.AllowAny]
    queryset = TenderDetails.objects.filter(deadline__gte=date.today(), status='active')
    filter_backends = [filters.SearchFilter, django_filters.DjangoFilterBackend]
    filterset_class = TenderDetailsFilter
    search_fields = [
        'title', 'description',
        'tag__title', 'tender_type__title', 'sector__title',
        'tender_category__title', 'country__title',
        'city__title'
    ]
    pagination_class = CustomPagination

    def list(self, request, tenderId):
        """
        Retrieves a list of suggested tenders based on the given tenderId.

        Args:
            - request (HttpRequest): The HTTP request object.
            - tenderId (int): The ID of the tender to retrieve suggestions for.

        Returns:
            Response: The HTTP response object containing the suggested tenders.

        Raises:
            TenderDetails.DoesNotExist: If the specified tenderId does not exist.
        """
        
        context = dict()
        if request.user:
            context = {"user": request.user}
        queryset = self.filter_queryset(self.get_queryset())
        try:
            tender_instance = TenderDetails.objects.get(id=tenderId)
            annotated_tender_details = TenderDetails.objects.filter(~Q(id=tender_instance.id)).annotate(
                matches=Value(0)
            ).annotate(
                matches=Case(
                    When(
                        budget_amount=tender_instance.budget_amount,
                        then=F('matches') + 1
                    ),
                    default=F('matches'),
                    output_field=IntegerField()
                )
            ).annotate(
                matches=Case(
                    When(
                        tag__in=tender_instance.tag.all(),
                        then=F('matches') + 1
                    ),
                    default=F('matches'),
                    output_field=IntegerField()
                )
            ).annotate(
                matches=Case(
                    When(
                        tender_category__in=tender_instance.tender_category.all(),
                        then=F('matches') + 1
                    ),
                    default=F('matches'),
                    output_field=IntegerField()
                )
            ).annotate(
                matches=Case(
                    When(
                        tender_type__in=tender_instance.tender_type.all(),
                        then=F('matches') + 1
                    ),
                    default=F('matches'),
                    output_field=IntegerField()
                )
            ).annotate(
                matches=Case(
                    When(
                        sector__in=tender_instance.sector.all(),
                        then=F('matches') + 1
                    ),
                    default=F('matches'),
                    output_field=IntegerField()
                )
            )
            tender = annotated_tender_details.filter(matches=4).order_by('-matches').distinct('matches')
            if tender.count() == 0:
                tender = annotated_tender_details.order_by('-matches').distinct('matches')
            page = self.paginate_queryset(tender)
            if page is not None:
                serializer = self.get_serializer(page, many=True, context=context)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(tender, many=True, context=context)
            return response.Response(serializer.data)
        except TenderDetails.DoesNotExist:
            return response.Response(
                data={"tender": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )


class ApplicationsDetailView(generics.GenericAPIView):
    """
    A view for retrieving the details of a specific application for a tender.

    Attributes:
        - serializer_class (GetAppliedTenderSerializers): The serializer class used for data serialization.
        - permission_classes ([permissions.IsAuthenticated]): List of permission classes that the view requires.
            In this case, only authenticated users are allowed to access the view.

    Methods:
        - get(request, applicationId): Retrieves the details of the specified application for a tender.

    Returns:
        - response.Response: A response object containing the application details or an error message.

    Raises:
        - Exception: If an error occurs during the retrieval process.
    """

    serializer_class = GetAppliedTenderApplicationSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, applicationId):
        context = dict()
        try:
            if applicationId:
                application_data = AppliedTender.objects.get(id=applicationId)
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
                application_status = AppliedTender.objects.get(id=applicationId)
                if application_status.tender.user == request.user:
                    message = "Successfully "
                    if action == "shortlisted":
                        if application_status.shortlisted_at:
                            message = "Already "
                        else:
                            application_status.shortlisted_at = datetime.now()
                            application_status.save()
                            if application_status.user.get_notification:
                                Notification.objects.create(
                                    user=application_status.user, tender_application=application_status,
                                    notification_type='shortlisted', created_by=request.user
                                )
                                if application_status.user.email:
                                    email_context = dict()
                                    if application_status.user.name:
                                        user_name = application_status.user.name
                                    else:
                                        user_name = application_status.user.email
                                    email_context["yourname"] = user_name
                                    email_context["notification_type"] = "shortlisted tender"
                                    email_context["job_instance"] = application_status.shortlisted_at
                                    if application_status.user.get_email:
                                        get_email_object(
                                            subject=f'Notification for shortlisted tender',
                                            email_template_name='email-templates/send-notification.html',
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
                                data={"message": "Please enter a reason"},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                    context['message'] = str(message) + str(action)
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
        except Exception as e:
            context["message"] = str(e)
            return response.Response(
                data=context,
                status=status.HTTP_400_BAD_REQUEST
            )


class TenderApplicationsView(generics.ListAPIView):
    """
    A view class that returns a list of AppliedTender instances.

    Attributes:
            - `serializer_class`: A serializer class used to serialize the AppliedTender instances.
            - `permission_classes`: A list of permission classes that a user must pass in order to access the view.
            - `queryset`: A QuerySet instance representing the list of AppliedTender instances. The queryset is not
                defined in the class, but it can be defined dynamically in the dispatch method.
            - `filter_backends`: A list of filter backend classes used to filter the queryset.
            - `search_fields`: A list of fields on which the search filtering is applied.
            - `pagination_class`: A pagination class that is used to paginate the result set.

    """
    serializer_class = AppliedTenderSerializers
    permission_classes = [permissions.IsAuthenticated]
    queryset = None
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    pagination_class = CustomPagination

    def list(self, request, tenderId):
        """
        Retrieve a list of tender applications for the specified tender.

        Args:
            request (HttpRequest): The HTTP request object.
            tenderId (int): The ID of the tender.

        Returns:
            A response containing the serialized data of tender applications.

        Raises:
            NotFound (HTTP 404): If the specified tender does not exist.
            Exception: If an unexpected error occurs.

        Permissions:
            - User must be authenticated.
            - User role must be "employer".
        """
        
        context = dict()
        if self.request.user.role == "employer":
            try:
                tender_instance = TenderDetails.objects.get(id=tenderId, user=request.user)
                filters = Q(tender=tender_instance)
                filter_list = self.request.GET.getlist('filter')
                blacklisted_user_list = []
                for data in BlackList.objects.all():
                    blacklisted_user_list.append(data.blacklisted_user)
                for filter_data in filter_list:
                    if filter_data == "rejected": filters = filters & ~Q(rejected_at=None)
                    if filter_data == "shortlisted": filters = filters & ~Q(shortlisted_at=None)
                    if filter_data == "blacklisted": filters = filters & Q(user__in=blacklisted_user_list)
                queryset = self.filter_queryset(AppliedTender.objects.filter(filters))
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page, many=True, context={"request": request})
                    serialized_response = self.get_paginated_response(serializer.data)
                    serialized_response.data['rejected_count'] = AppliedTender.objects.filter(tender=tender_instance).filter(
                        ~Q(rejected_at=None)).count()
                    serialized_response.data['shortlisted_count'] = AppliedTender.objects.filter(tender=tender_instance).filter(
                        ~Q(shortlisted_at=None)).count()
                    user_list = []
                    for data in AppliedTender.objects.filter(job=tender_instance):
                        user_list.append(data.user)
                    serialized_response.data['blacklisted_count'] = BlackList.objects.filter(
                        blacklisted_user__in=user_list).order_by('blacklisted_user').distinct(
                        'blacklisted_user').count()
                        
                    return response.Response(data=serialized_response.data, status=status.HTTP_200_OK)
                serializer = self.get_serializer(queryset, many=True, context={"request": request})
                return response.Response(serializer.data)
            except TenderDetails.DoesNotExist:
                return response.Response(
                    data={"tender": "Does Not Exist"},
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
    A view class that returns a list of AppliedTender instances.

    Attributes:
            - `serializer_class`: A serializer class used to serialize the AppliedTender instances.
            - `permission_classes`: A list of permission classes that a user must pass in order to access the view.
            - `queryset`: A QuerySet instance representing the list of AppliedTender instances. The queryset is not
                defined in the class, but it can be defined dynamically in the dispatch method.
            - `filter_backends`: A list of filter backend classes used to filter the queryset.
            - `search_fields`: A list of fields on which the search filtering is applied.
            - `pagination_class`: A pagination class that is used to paginate the result set.

    """
    serializer_class = AppliedTenderSerializers
    permission_classes = [permissions.IsAuthenticated]
    queryset = None
    filter_backends = [filters.SearchFilter]
    search_fields = ['tender__title', 'user__email', 'user__name']
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
            except TenderDetails.DoesNotExist:
                return response.Response(
                    data={"tender": "Does Not Exist"},
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
        A method that returns a queryset of `AppliedTender instances`. It filters the queryset based on the `employer jobs`
        provided in the `request query parameters`.

        Args:
            **kwargs: A dictionary of keyword arguments.

        Returns:
            QuerySet: A filtered queryset of AppliedTender instances.

        """
        tender_data = TenderDetails.objects.filter(user=self.request.user.id)
        return AppliedTender.objects.filter(tender__in=tender_data)

