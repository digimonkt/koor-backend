from datetime import date

from django_filters import rest_framework as django_filters

from rest_framework import (
    status, generics, serializers,
    response, permissions, filters
)

from core.pagination import CustomPagination

from tenders.models import TenderDetails
from tenders.filters import TenderDetailsFilter
from tenders.serializers import (
    TendersSerializers, TendersDetailSerializers,
    TenderFiltersSerializers
)


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
    queryset = TenderDetails.objects.filter(deadline__gte=date.today())
    filter_backends = [filters.SearchFilter, django_filters.DjangoFilterBackend]
    filterset_class = TenderDetailsFilter
    search_fields = [
        'title', 'description',
        'tag__title', 'tender_type', 'sector',
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
        if tenderCategory:
            queryset = queryset.filter(tender_category__title__in=tenderCategory).distinct()
        if tag:
            queryset = queryset.filter(tag__title__in=tag).distinct()
        if sector:
            queryset = queryset.filter(sector__in=sector).distinct()
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
                job_data = TenderDetails.objects.get(id=tenderId)
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
