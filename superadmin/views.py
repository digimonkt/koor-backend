from rest_framework import (
    status, generics, serializers,
    response, permissions, filters
)

from core.pagination import CustomPagination

from project_meta.models import (
    Country, City
)

from .serializers import (
    CountrySerializers, CitySerializers
)


class CountryView(generics.ListAPIView):
    """
    A view for displaying a list of countries.

    Attributes:
        - permission_classes ([permissions.IsAuthenticated]): List of permission classes that the view requires. In this
            case, only authenticated users are allowed to access the view.

        - serializer_class (CountrySerializers): The serializer class used for data validation and serialization.

        - queryset (QuerySet): The queryset that the view should use to retrieve the countries. By default, it is set
            to retrieve all countries using `Country.objects.all()`.

        - filter_backends ([filters.SearchFilter]): List of filter backends to use for filtering the queryset. In this
            case, only `SearchFilter` is used.

        - search_fields (list): List of fields to search for in the queryset. In this case, the field is "title".

        - pagination_class (CustomPagination): The pagination class to use for paginating the queryset results.

    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CountrySerializers
    queryset = Country.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    pagination_class = CustomPagination

    def post(self, request):
        """
        Handle POST request to create a new country.
        The request must contain valid data for the country to be created.

        Only users with `admin` role and `is_staff` attribute set to True are authorized to create a country.

        Returns:
            - HTTP 201 CREATED with a message "Country added successfully" if the country is created successfully.
            - HTTP 400 BAD REQUEST with error message if data validation fails.
            - HTTP 401 UNAUTHORIZED with a message "You do not have permission to perform this action." if the user is not authorized.

        Raises:
            Exception: If an unexpected error occurs during the request handling.
        """

        context = dict()
        serializer = self.serializer_class(data=request.data)
        try:
            if self.request.user.role == "admin" and self.request.user.is_staff:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                context["message"] = "Country added successfully."
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
            context['message'] = str(e)
            return response.Response(
                data=context,
                status=status.HTTP_400_BAD_REQUEST
            )

class CityView(generics.ListAPIView):
    """
    A class-based view that provides the list of cities in the database.
    
    This view is based on the generic ListAPIView provided by Django Rest Framework's generics module.
    It requires the user to be authenticated before accessing the list of cities. The list of cities is
    represented by a serializer class (CitySerializers) which defines how the data is represented in the API.
    The list of cities is retrieved using the queryset attribute set to City.objects.all().
    The view also supports searching for cities by the title field using the SearchFilter backend and search_fields attribute.
    The view uses the CustomPagination class for pagination.

    Attributes:
        - permission_classes (list): List of permission classes used to check user authentication.
        - serializer_class (CitySerializers): Serializer class used to represent the cities in the API.
        - queryset (City.objects.all()): Queryset used to retrieve the list of cities.
        - filter_backends (list): List of filter backends used to search the cities.
        - search_fields (list): List of fields that can be searched in the cities.
        - pagination_class (CustomPagination): Pagination class used to handle pagination in the API.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CitySerializers
    queryset = City.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    pagination_class = CustomPagination

    def post(self, request):
        context = dict()
        serializer = self.serializer_class(data=request.data)
        try:
            if self.request.user.role == "admin" and self.request.user.is_staff:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                context["message"] = "City added successfully."
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
            context['message'] = str(e)
            return response.Response(
                data=context,
                status=status.HTTP_400_BAD_REQUEST
            )
