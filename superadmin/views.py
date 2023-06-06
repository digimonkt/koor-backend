import io, csv, os, pathlib
from datetime import datetime, date, timedelta
from django.db.models import Exists, OuterRef

from django.db.models import Q
from django_filters import rest_framework as django_filters

from rest_framework import (
    status, generics, serializers,
    response, permissions, filters
)
from rest_framework.pagination import LimitOffsetPagination

from core.middleware import JWTMiddleware
from core.pagination import CustomPagination

from jobs.models import (
    JobCategory, JobDetails,
    JobSubCategory
)
from jobs.filters import JobDetailsFilter

from users.filters import UsersFilter
from user_profile.models import EmployerProfile
from users.models import UserSession, User

from project_meta.models import (
    Country, City, EducationLevel,
    Language, Skill, Tag,
    AllCountry, AllCity,
    Choice, OpportunityType
)

from tenders.models import TenderCategory, TenderDetails
from tenders.filters import TenderDetailsFilter

from .models import (
    Content, ResourcesContent, SocialUrl,
    AboutUs, FaqCategory, FAQ
)
from .serializers import (
    CountrySerializers, CitySerializers, JobCategorySerializers,
    EducationLevelSerializers, LanguageSerializers, SkillSerializers,
    TagSerializers, ChangePasswordSerializers, ContentSerializers,
    CandidatesSerializers, JobListSerializers, UserCountSerializers,
    DashboardCountSerializers, TenderCategorySerializers, 
    JobSubCategorySerializers, OpportunityTypeSerializers,
    AllCountrySerializers, GetJobSubCategorySerializers,
    AllCitySerializers, GetCitySerializers,
    ChoiceSerializers, TenderListSerializers, ResourcesSerializers,
    CreateResourcesSerializers, SocialUrlSerializers,
    AboutUsSerializers, UpdateAboutUsSerializers, FaqCategorySerializers,
    FAQSerializers, CreateFAQSerializers
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

    """
    permission_classes = [permissions.AllowAny]
    serializer_class = CountrySerializers
    queryset = Country.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    pagination_class = CustomPagination

    def list(self, request):
        if self.request.user.is_staff:
            queryset = self.filter_queryset(self.get_queryset())
        else:
            queryset = self.filter_queryset(self.get_queryset().filter(~Q(project_meta_city_country=None)))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def post(self, request):
        """
        Handle POST request to create a new country.
        The request must contain valid data for the country to be created.

        Only users with `is_staff` attribute set to True are authorized to create a country.

        Returns:
            - HTTP 201 CREATED with a message "Country added successfully" if the country is created successfully.
            - HTTP 400 BAD REQUEST with error message if data validation fails.
            - HTTP 401 UNAUTHORIZED with a message "You do not have permission to perform this action." if the user is
            not authorized.

        Raises:
            Exception: If an unexpected error occurs during the request handling.
        """

        context = dict()
        country_instance = None
        serializer = self.serializer_class(data=request.data)
        try:
            if self.request.user.is_staff:
                serializer.is_valid(raise_exception=True)
                if Country.all_objects.filter(title__iexact=serializer.validated_data['title'],
                                              is_removed=True).exists():
                    Country.all_objects.filter(title__iexact=serializer.validated_data['title'],
                                               is_removed=True).update(
                        is_removed=False)
                    country_instance = Country.all_objects.get(title__iexact=serializer.validated_data['title'], is_removed=False)
                    
                else:
                    serializer.save()
                context["data"] = serializer.data
                if country_instance:
                    context["data"]['id'] = str(country_instance.id)
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

    def delete(self, request, countryId):
        """
        Deletes an Country object with the given ID if the authenticated user is a job seeker and owns the
        Country.
        Args:
            request: A DRF request object.
            educationId: An integer representing the ID of the Country to be deleted.
        Returns:
            A DRF response object with a success or error message and appropriate status code.
        """
        context = dict()
        if self.request.user.is_staff:
            try:
                Country.objects.get(id=countryId).delete()
                context['message'] = "Deleted Successfully"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except Country.DoesNotExist:
                return response.Response(
                    data={"Country": "Does Not Exist"},
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


class CityView(generics.ListAPIView):
    """
    A view for displaying a list of Cities.

    Attributes:
        - permission_classes ([permissions.IsAuthenticated]): List of permission classes that the view requires. In this
            case, only authenticated users are allowed to access the view.

        - serializer_class (CitySerializers): The serializer class used for data validation and serialization.

        - queryset (QuerySet): The queryset that the view should use to retrieve the countries. By default, it is set
            to retrieve all countries using `City.objects.all()`.

        - filter_backends ([filters.SearchFilter]): List of filter backends to use for filtering the queryset. In this
            case, only `SearchFilter` is used.

        - search_fields (list): List of fields to search for in the queryset. In this case, the field is "title".

    """

    permission_classes = [permissions.AllowAny]
    serializer_class = GetCitySerializers
    queryset = City.objects.filter(country__is_removed=False)
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    pagination_class = CustomPagination

    def list(self, request):
        country_id = request.GET.get('countryId', None)
        if country_id:
            queryset = self.filter_queryset(self.get_queryset().filter(country_id=country_id))
        else:
            queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def post(self, request):
        """
        Handle POST request to create a new city.
        The request must contain valid data for the city to be created.

        Only users with `is_staff` attribute set to True are authorized to create a city.

        Returns:
            - HTTP 201 CREATED with a message "City added successfully" if the city is created successfully.
            - HTTP 400 BAD REQUEST with error message if data validation fails.
            - HTTP 401 UNAUTHORIZED with a message "You do not have permission to perform this action." if the user is
            not authorized.

        Raises:
            Exception: If an unexpected error occurs during the request handling.
        """
        context = dict()
        serializer = CitySerializers(data=request.data)
        try:
            if self.request.user.is_staff:
                serializer.is_valid(raise_exception=True)
                if City.all_objects.filter(title__iexact=serializer.validated_data['title'],
                                           country__title=serializer.validated_data['country_name'], is_removed=True).exists():
                    City.all_objects.filter(title__iexact=serializer.validated_data['title'],
                                            country__title=serializer.validated_data['country_name'], is_removed=True).update(
                        is_removed=False)
                    city = City.objects.get(title__iexact=serializer.validated_data['title'],
                                            country__title=serializer.validated_data['country_name'], is_removed=False)
                else:
                    city = serializer.save()
                context["data"] = {'id': str(city.id), 'title': str(city.title), 'country': str(city.country.id)}
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

    def delete(self, request, cityId):
        """
        Deletes an City object with the given ID if the authenticated user is a job seeker and owns the
        City.
        Args:
            request: A DRF request object.
            educationId: An integer representing the ID of the City to be deleted.
        Returns:
            A DRF response object with a success or error message and appropriate status code.
        """
        context = dict()
        if self.request.user.is_staff:
            try:
                City.objects.get(id=cityId).delete()
                context['message'] = "Deleted Successfully"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except City.DoesNotExist:
                return response.Response(
                    data={"City": "Does Not Exist"},
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


class JobCategoryView(generics.ListAPIView):
    """
    A view for displaying a list of job categories.

    Attributes:
        - permission_classes ([permissions.IsAuthenticated]): List of permission classes that the view requires. In this
            case, only authenticated users are allowed to access the view.

        - serializer_class (JobCategorySerializers): The serializer class used for data validation and serialization.

        - queryset (QuerySet): The queryset that the view should use to retrieve the countries. By default, it is set
            to retrieve all countries using `JobCategory.objects.all()`.

        - filter_backends ([filters.SearchFilter]): List of filter backends to use for filtering the queryset. In this
            case, only `SearchFilter` is used.

        - search_fields (list): List of fields to search for in the queryset. In this case, the field is "title".

    """

    permission_classes = [permissions.AllowAny]
    serializer_class = JobCategorySerializers
    queryset = JobCategory.objects.annotate(has_subcategory=Exists(JobSubCategory.objects.filter(category_id=OuterRef('id'))))
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    pagination_class = CustomPagination

    def list(self, request):
        if self.request.user.is_staff:
            queryset = self.filter_queryset(self.get_queryset())
        else:
            queryset = self.filter_queryset(self.get_queryset().filter(has_subcategory=True))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def post(self, request):
        """
        Handle POST request to create a new job category.
        The request must contain valid data for the job category to be created.

        Only users with `is_staff` attribute set to True are authorized to create a job category.

        Returns:
            - HTTP 201 CREATED with a message "JobCategory added successfully" if the job category is created
            successfully.
            - HTTP 400 BAD REQUEST with error message if data validation fails.
            - HTTP 401 UNAUTHORIZED with a message "You do not have permission to perform this action." if the user is
            not authorized.

        Raises:
            Exception: If an unexpected error occurs during the request handling.
        """
        context = dict()
        serializer = self.serializer_class(data=request.data)
        try:
            if self.request.user.is_staff:
                serializer.is_valid(raise_exception=True)
                if JobCategory.all_objects.filter(title__iexact=serializer.validated_data['title'],
                                                  is_removed=True).exists():
                    JobCategory.all_objects.filter(title__iexact=serializer.validated_data['title'],
                                                   is_removed=True).update(
                        is_removed=False)
                else:
                    serializer.save()
                context["data"] = serializer.data
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

    def delete(self, request, jobCategoryId):
        """
        Deletes an JobCategory object with the given ID if the authenticated user is a job seeker and owns the
        JobCategory.
        Args:
            request: A DRF request object.
            educationId: An integer representing the ID of the JobCategory to be deleted.
        Returns:
            A DRF response object with a success or error message and appropriate status code.
        """
        context = dict()
        if self.request.user.is_staff:
            try:
                JobCategory.objects.get(id=jobCategoryId).delete()
                context['message'] = "Deleted Successfully"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except JobCategory.DoesNotExist:
                return response.Response(
                    data={"jobCategoryId": "Does Not Exist"},
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

    def put(self, request, jobCategoryId):
        """
        Update an `JobCategory` instance with the provided data.

        Args:
            - `request (django.http.request.Request)`: The HTTP request object.
            - `jobCategoryId (int)`: The ID of the `JobCategory` instance to update.

        Returns:
            - `django.http.response.Response`: An HTTP response object containing the updated data
            and appropriate status code.

        Raises:
            - `serializers.ValidationError`: If the provided data is invalid.
            - `JobCategory.DoesNotExist`: If the JobCategory instance with the given ID does not exist.
            - `Exception`: If any other error occurs during the update process.
        """

        context = dict()
        try:
            job_category_instance = JobCategory.all_objects.get(id=jobCategoryId)
            serializer = self.serializer_class(data=request.data, instance=job_category_instance, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                if serializer.update(job_category_instance, serializer.validated_data):
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
        except JobCategory.DoesNotExist:
            return response.Response(
                data={"jobCategoryId": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["message"] = e
            return response.Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
            )


class EducationLevelView(generics.ListAPIView):
    """
    A view for displaying a list of education levels .

    Attributes:
        - permission_classes ([permissions.IsAuthenticated]): List of permission classes that the view requires. In this
            case, only authenticated users are allowed to access the view.

        - serializer_class (EducationLevelSerializers): The serializer class used for data validation and serialization.

        - queryset (QuerySet): The queryset that the view should use to retrieve the countries. By default, it is set
            to retrieve all countries using `EducationLevel.objects.all()`.

        - filter_backends ([filters.SearchFilter]): List of filter backends to use for filtering the queryset. In this
            case, only `SearchFilter` is used.

        - search_fields (list): List of fields to search for in the queryset. In this case, the field is "title".

    """

    permission_classes = [permissions.AllowAny]
    serializer_class = EducationLevelSerializers
    queryset = EducationLevel.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    pagination_class = CustomPagination

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def post(self, request):
        """
        Handle POST request to create a new education level.
        The request must contain valid data for the education level to be created.

        Only users with `is_staff` attribute set to True are authorized to create a education level.

        Returns:
            - HTTP 201 CREATED with added education level data (id, title) if the education level is created
            successfully.
            - HTTP 400 BAD REQUEST with error message if data validation fails.
            - HTTP 401 UNAUTHORIZED with a message "You do not have permission to perform this action." if the user is
            not authorized.

        Raises:
            Exception: If an unexpected error occurs during the request handling.
        """
        context = dict()
        serializer = self.serializer_class(data=request.data)
        try:
            if self.request.user.is_staff:
                serializer.is_valid(raise_exception=True)
                if EducationLevel.all_objects.filter(title__iexact=serializer.validated_data['title'],
                                                     is_removed=True).exists():
                    EducationLevel.all_objects.filter(title__iexact=serializer.validated_data['title'],
                                                      is_removed=True).update(
                        is_removed=False)
                else:
                    serializer.save()
                context["data"] = serializer.data
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

    def delete(self, request, educationLevelId):
        """
        Deletes an EducationLevel object with the given ID if the authenticated user is a job seeker and owns the
        EducationLevel.
        Args:
            request: A DRF request object.
            educationId: An integer representing the ID of the EducationLevel to be deleted.
        Returns:
            A DRF response object with a success or error message and appropriate status code.
        """
        context = dict()
        if self.request.user.is_staff:
            try:
                EducationLevel.objects.get(id=educationLevelId).delete()
                context['message'] = "Deleted Successfully"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except EducationLevel.DoesNotExist:
                return response.Response(
                    data={"educationLevelId": "Does Not Exist"},
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

    def put(self, request, educationLevelId):
        """
        Update an `EducationLevel` instance with the provided data.

        Args:
            - `request (django.http.request.Request)`: The HTTP request object.
            - `educationLevelId (int)`: The ID of the `EducationLevel` instance to update.

        Returns:
            - `django.http.response.Response`: An HTTP response object containing the updated data
            and appropriate status code.

        Raises:
            - `serializers.ValidationError`: If the provided data is invalid.
            - `EducationLevel.DoesNotExist`: If the EducationLevel instance with the given ID does not exist.
            - `Exception`: If any other error occurs during the update process.
        """

        context = dict()
        try:
            education_level_instance = EducationLevel.all_objects.get(id=educationLevelId)
            serializer = self.serializer_class(data=request.data, instance=education_level_instance, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                if serializer.update(education_level_instance, serializer.validated_data):
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
        except EducationLevel.DoesNotExist:
            return response.Response(
                data={"educationLevelId": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["message"] = e
            return response.Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
            )


class LanguageView(generics.ListAPIView):
    """
    A view for displaying a list of languages .

    Attributes:
        - permission_classes ([permissions.IsAuthenticated]): List of permission classes that the view requires. In this
            case, only authenticated users are allowed to access the view.

        - serializer_class (LanguageSerializers): The serializer class used for data validation and serialization.

        - queryset (QuerySet): The queryset that the view should use to retrieve the countries. By default, it is set
            to retrieve all countries using `Language.objects.all()`.

        - filter_backends ([filters.SearchFilter]): List of filter backends to use for filtering the queryset. In this
            case, only `SearchFilter` is used.

        - search_fields (list): List of fields to search for in the queryset. In this case, the field is "title".

    """

    permission_classes = [permissions.AllowAny]
    serializer_class = LanguageSerializers
    queryset = Language.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    pagination_class = CustomPagination

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def post(self, request):
        """
        Handle POST request to create a new language.
        The request must contain valid data for the language to be created.

        Only users with `is_staff` attribute set to True are authorized to create a language.

        Returns:
            - HTTP 201 CREATED with added language data (id, title) if the language is created successfully.
            - HTTP 400 BAD REQUEST with error message if data validation fails.
            - HTTP 401 UNAUTHORIZED with a message "You do not have permission to perform this action." if the user is
            not authorized.

        Raises:
            Exception: If an unexpected error occurs during the request handling.
        """
        context = dict()
        serializer = self.serializer_class(data=request.data)
        try:
            if self.request.user.is_staff:
                serializer.is_valid(raise_exception=True)
                if Language.all_objects.filter(title__iexact=serializer.validated_data['title'],
                                               is_removed=True).exists():
                    Language.all_objects.filter(title__iexact=serializer.validated_data['title'],
                                                is_removed=True).update(
                        is_removed=False)
                else:
                    serializer.save()
                context["data"] = serializer.data
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

    def delete(self, request, languageId):
        """
        Deletes an Language object with the given ID if the authenticated user is a job seeker and owns the
        Language.
        Args:
            request: A DRF request object.
            educationId: An integer representing the ID of the Language to be deleted.
        Returns:
            A DRF response object with a success or error message and appropriate status code.
        """
        context = dict()
        if self.request.user.is_staff:
            try:
                Language.objects.get(id=languageId).delete()
                context['message'] = "Deleted Successfully"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except Language.DoesNotExist:
                return response.Response(
                    data={"Language": "Does Not Exist"},
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

    def put(self, request, languageId):
        """
        Update a `Language` instance with the provided data.

        Args:
            - `request (django.http.request.Request)`: The HTTP request object.
            - `languageId (int)`: The ID of the `Language` instance to update.

        Returns:
            - `django.http.response.Response`: An HTTP response object containing the updated data
            and appropriate status code.

        Raises:
            - `serializers.ValidationError`: If the provided data is invalid.
            - `Language.DoesNotExist`: If the Language instance with the given ID does not exist.
            - `Exception`: If any other error occurs during the update process.

        """

        context = dict()
        try:
            language_instance = Language.all_objects.get(id=languageId)
            serializer = self.serializer_class(data=request.data, instance=language_instance, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                if serializer.update(language_instance, serializer.validated_data):
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
        except Language.DoesNotExist:
            return response.Response(
                data={"languageId": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["message"] = e
            return response.Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
            )


class SkillView(generics.ListAPIView):
    """
    A view for displaying a list of skills .

    Attributes:
        - permission_classes ([permissions.IsAuthenticated]): List of permission classes that the view requires. In this
            case, only authenticated users are allowed to access the view.

        - serializer_class (SkillSerializers): The serializer class used for data validation and serialization.

        - queryset (QuerySet): The queryset that the view should use to retrieve the countries. By default, it is set
            to retrieve all countries using `Skill.objects.all()`.

        - filter_backends ([filters.SearchFilter]): List of filter backends to use for filtering the queryset. In this
            case, only `SearchFilter` is used.

        - search_fields (list): List of fields to search for in the queryset. In this case, the field is "title".

    """

    permission_classes = [permissions.AllowAny]
    serializer_class = SkillSerializers
    queryset = Skill.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    pagination_class = CustomPagination

    def list(self, request):
        exclude = request.GET.get('exclude', None)
        if exclude:
            queryset = self.filter_queryset(self.get_queryset().exclude(title__in=exclude.split(",")))
        else:
            queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def post(self, request):
        """
        Handle POST request to create a new skill.
        The request must contain valid data for the skill to be created.

        Only users with `is_staff` attribute set to True are authorized to create a skill.

        Returns:
            - HTTP 201 CREATED with added skill data (id, title) if the skill is created successfully.
            - HTTP 400 BAD REQUEST with error message if data validation fails.
            - HTTP 401 UNAUTHORIZED with a message "You do not have permission to perform this action." if the user is
            not authorized.

        Raises:
            Exception: If an unexpected error occurs during the request handling.
        """
        context = dict()
        serializer = self.serializer_class(data=request.data)
        try:
            if self.request.user.is_staff:
                serializer.is_valid(raise_exception=True)
                if Skill.all_objects.filter(title__iexact=serializer.validated_data['title'], is_removed=True).exists():
                    Skill.all_objects.filter(title__iexact=serializer.validated_data['title'], is_removed=True).update(
                        is_removed=False)
                else:
                    serializer.save()
                context["data"] = serializer.data
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

    def delete(self, request, skillId):
        """
        Deletes an Skill object with the given ID if the authenticated user is a job seeker and owns the
        Skill.
        Args:
            request: A DRF request object.
            educationId: An integer representing the ID of the Skill to be deleted.
        Returns:
            A DRF response object with a success or error message and appropriate status code.
        """
        context = dict()
        if self.request.user.is_staff:
            try:
                Skill.objects.get(id=skillId).delete()
                context['message'] = "Deleted Successfully"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except Skill.DoesNotExist:
                return response.Response(
                    data={"skill": "Does Not Exist"},
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

    def put(self, request, skillId):
        """
        Update a `Skill` instance with the provided data.

        Args:
            - `request (django.http.request.Request)`: The HTTP request object.
            - `skillId (int)`: The ID of the `Skill` instance to update.

        Returns:
            - `django.http.response.Response`: An HTTP response object containing the updated data
            and appropriate status code.

        Raises:
            - `serializers.ValidationError`: If the provided data is invalid.
            - `Skill.DoesNotExist`: If the Skill instance with the given ID does not exist.
            - `Exception`: If any other error occurs during the update process.

        """

        context = dict()
        try:
            skill_instance = Skill.all_objects.get(id=skillId)
            serializer = self.serializer_class(data=request.data, instance=skill_instance, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                if serializer.update(skill_instance, serializer.validated_data):
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
        except Skill.DoesNotExist:
            return response.Response(
                data={"skillId": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["message"] = e
            return response.Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
            )


class TagView(generics.ListAPIView):
    """
    A view for displaying a list of tags .

    Attributes:
        - permission_classes ([permissions.IsAuthenticated]): List of permission classes that the view requires. In this
            case, only authenticated users are allowed to access the view.

        - serializer_class (TagSerializers): The serializer class used for data validation and serialization.

        - queryset (QuerySet): The queryset that the view should use to retrieve the countries. By default, it is set
            to retrieve all countries using `Tag.objects.all()`.

        - filter_backends ([filters.SearchFilter]): List of filter backends to use for filtering the queryset. In this
            case, only `SearchFilter` is used.

        - search_fields (list): List of fields to search for in the queryset. In this case, the field is "title".

    """

    permission_classes = [permissions.AllowAny]
    serializer_class = TagSerializers
    queryset = Tag.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    pagination_class = CustomPagination

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def post(self, request):
        """
        Handle POST request to create a new tag.
        The request must contain valid data for the tag to be created.

        Only users with `is_staff` attribute set to True are authorized to create a tag.

        Returns:
            - HTTP 201 CREATED with added tag data (id, title) if the tag is created successfully.
            - HTTP 400 BAD REQUEST with error message if data validation fails.
            - HTTP 401 UNAUTHORIZED with a message "You do not have permission to perform this action." if the user is
            not authorized.

        Raises:
            Exception: If an unexpected error occurs during the request handling.
        """
        context = dict()
        serializer = self.serializer_class(data=request.data)
        try:
            if self.request.user.is_staff:
                serializer.is_valid(raise_exception=True)
                if Tag.all_objects.filter(title__iexact=serializer.validated_data['title'], is_removed=True).exists():
                    Tag.all_objects.filter(title__iexact=serializer.validated_data['title'], is_removed=True).update(
                        is_removed=False)
                else:
                    serializer.save()
                context["data"] = serializer.data
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

    def delete(self, request, tagId):
        """
        Deletes an Tag object with the given ID if the authenticated user is a job seeker and owns the
        Tag.
        Args:
            request: A DRF request object.
            educationId: An integer representing the ID of the Tag to be deleted.
        Returns:
            A DRF response object with a success or error message and appropriate status code.
        """
        context = dict()
        if self.request.user.is_staff:
            try:
                Tag.objects.get(id=tagId).delete()
                context['message'] = "Deleted Successfully"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except Tag.DoesNotExist:
                return response.Response(
                    data={"tag": "Does Not Exist"},
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

    def put(self, request, tagId):
        """
        Update a `Tag` instance with the provided data.

        Args:
            - `request (django.http.request.Request)`: The HTTP request object.
            - `tagId (int)`: The ID of the `Tag` instance to update.

        Returns:
            - `django.http.response.Response`: An HTTP response object containing the updated data
            and appropriate status code.

        Raises:
            - `serializers.ValidationError`: If the provided data is invalid.
            - `Tag.DoesNotExist`: If the Tag instance with the given ID does not exist.
            - `Exception`: If any other error occurs during the update process.

        """

        context = dict()
        try:
            tag_instance = Tag.all_objects.get(id=tagId)
            serializer = self.serializer_class(data=request.data, instance=tag_instance, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                if serializer.update(tag_instance, serializer.validated_data):
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
        except Tag.DoesNotExist:
            return response.Response(
                data={"tagId": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["message"] = e
            return response.Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
            )


class ChangePasswordView(generics.GenericAPIView):
    """
    A class-based view to handle changing password for an authenticated user. Only staff users are allowed to change
    password.

    `Attributes`:
        - `permission_classes (list)`: A list of permission classes that are required for this view. In this case, only
            authenticated users are allowed.
        - `serializer_class`: A serializer class that will be used to validate the request data.

    `Methods`:
        - `patch(request)`: A method that handles the HTTP PATCH requests. It receives a request object, validates the
            request data using the serializer, and updates the user password if the user is staff. Returns a response
            object with a message and HTTP status code.

    `Raises`:
        - `serializers.ValidationError`: If the request data is invalid.
        - `Exception`: If any other error occurs while processing the request.

    `Returns`:
        - A response object with a message and HTTP status code indicating the success or failure of the password update
        operation.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializers

    def patch(self, request):

        response_context = dict()
        try:
            if self.request.user.is_staff:
                context = {"user": request.user}
                serializer = self.serializer_class(data=request.data, context=context)
                serializer.is_valid(raise_exception=True)
                refresh_token = request.headers.get('x-refresh')
                payload = JWTMiddleware.decode_token(refresh_token)
                UserSession.objects.filter(id=payload.get('session_id')).update(expire_at=datetime.now())
                response_context["message"] = "Password update successfully."
                return response.Response(
                    data=response_context,
                    status=status.HTTP_200_OK
                )
            else:
                response_context['message'] = "You do not have permission to perform this action."
                return response.Response(
                    data=response_context,
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except serializers.ValidationError:
            return response.Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            response_context['message'] = str(e)
            return response.Response(
                data=response_context,
                status=status.HTTP_400_BAD_REQUEST
            )


class UserRightsView(generics.GenericAPIView):
    """
    View to retrieve the user rights.

    This view extends the GenericAPIView class from Django Rest Framework and defines the permission_classes and
    serializer_class attributes to control the access permissions and serialization of data.

    Attributes:
        - `permission_classes (list)`: A list of permission classes that allow any user to access the view.
        - `serializer_class (ContentSerializers)`: The serializer class used to serialize the data retrieved from
        the view.

    """

    permission_classes = [permissions.AllowAny]
    serializer_class = ContentSerializers

    def get(self, request):
        """
        Retrieve the user rights content.

        This method retrieves the user rights content from the database using the Content model, serializes it using the
        serializer_class attribute, and returns it as a response.

        Args:
            - `request (HttpRequest)`: The HTTP request sent to the view.

        Returns:
            - A Response object with the user rights content as data and a 200 status code if the content is found in
            the database.
            - A Response object with a description field as data and a 404 status code if the content is not found in
            the database.
            - A Response object with an error message as data and a 400 status code if an exception occurs.

        Raises:
            None.

        """

        response_context = dict()
        try:
            content_instance = Content.objects.get(title="User Rights")
            get_data = self.serializer_class(content_instance)
            response_context = get_data.data
            return response.Response(
                data=response_context,
                status=status.HTTP_200_OK
            )
        except Content.DoesNotExist:
            return response.Response(
                data={"description": None},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            response_context['message'] = str(e)
            return response.Response(
                data=response_context,
                status=status.HTTP_400_BAD_REQUEST
            )

    def patch(self, request):
        """
        Handle PATCH requests to update a Content object.

        Args:
            - `request (Request)`: The incoming PATCH request.

        Returns:
            - A Response object with a success message if the user is a staff member and the update was successful,
              or an error message if the user does not have permission to perform the action or the data provided in
              the request is invalid.

        Raises:
            - N/A

        Behavior:
            - This function first checks whether the user making the request is a staff member.
            - If so, it looks for an existing Content object with the title "User Rights".
            - If one exists, it updates that object with the data provided in the request.
            - If not, it either finds a previously removed object with that title and un-removes it, or creates a new
              object with that title.
            - It then attempts to validate the provided data and update the Content object with that data.
            - If the update is successful, it returns a success message.
            - If the provided data is invalid, it returns an error message.
            - If the user is not a staff member, it returns an error message.
        """

        context = dict()
        if self.request.user.is_staff:

            if Content.objects.filter(title="User Rights").exists():
                instance = Content.objects.get(title="User Rights")
            else:
                if Content.all_objects.filter(title="User Rights", is_removed=True).exists():
                    instance = Content.all_objects.get(title="User Rights", is_removed=True)
                    instance.is_removed = False
                else:
                    instance = Content.objects.create(title="User Rights")
                instance.save()
            serializer = self.serializer_class(data=request.data, instance=instance, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                if serializer.update(instance, serializer.validated_data):
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


class PrivacyPolicyView(generics.GenericAPIView):
    """
    View to retrieve the user rights.

    This view extends the GenericAPIView class from Django Rest Framework and defines the permission_classes and
    serializer_class attributes to control the access permissions and serialization of data.

    Attributes:
        - `permission_classes (list)`: A list of permission classes that allow any user to access the view.
        - `serializer_class (ContentSerializers)`: The serializer class used to serialize the data retrieved from
        the view.

    """

    permission_classes = [permissions.AllowAny]
    serializer_class = ContentSerializers

    def get(self, request):
        """
        Retrieve the user rights content.

        This method retrieves the user rights content from the database using the Content model, serializes it using the
        serializer_class attribute, and returns it as a response.

        Args:
            - `request (HttpRequest)`: The HTTP request sent to the view.

        Returns:
            - A Response object with the user rights content as data and a 200 status code if the content is found in
            the database.
            - A Response object with a description field as data and a 404 status code if the content is not found in
            the database.
            - A Response object with an error message as data and a 400 status code if an exception occurs.

        Raises:
            None.

        """

        response_context = dict()
        try:
            content_instance = Content.objects.get(title="Privacy Policy")
            get_data = self.serializer_class(content_instance)
            response_context = get_data.data
            return response.Response(
                data=response_context,
                status=status.HTTP_200_OK
            )
        except Content.DoesNotExist:
            return response.Response(
                data={"description": None},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            response_context['message'] = str(e)
            return response.Response(
                data=response_context,
                status=status.HTTP_400_BAD_REQUEST
            )

    def patch(self, request):
        """
        Handle PATCH requests to update a Content object.

        Args:
            - `request (Request)`: The incoming PATCH request.

        Returns:
            - A Response object with a success message if the user is a staff member and the update was successful,
              or an error message if the user does not have permission to perform the action or the data provided in
              the request is invalid.

        Raises:
            - N/A

        Behavior:
            - This function first checks whether the user making the request is a staff member.
            - If so, it looks for an existing Content object with the title "Privacy Policy".
            - If one exists, it updates that object with the data provided in the request.
            - If not, it either finds a previously removed object with that title and un-removes it, or creates a new
              object with that title.
            - It then attempts to validate the provided data and update the Content object with that data.
            - If the update is successful, it returns a success message.
            - If the provided data is invalid, it returns an error message.
            - If the user is not a staff member, it returns an error message.
        """

        context = dict()
        if self.request.user.is_staff:

            if Content.objects.filter(title="Privacy Policy").exists():
                instance = Content.objects.get(title="Privacy Policy")
            else:
                if Content.all_objects.filter(title="Privacy Policy", is_removed=True).exists():
                    instance = Content.all_objects.get(title="Privacy Policy", is_removed=True)
                    instance.is_removed = False
                else:
                    instance = Content.objects.create(title="Privacy Policy")
                instance.save()
            serializer = self.serializer_class(data=request.data, instance=instance, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                if serializer.update(instance, serializer.validated_data):
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


class CandidatesListView(generics.ListAPIView):
    """
    API view for listing job seekers by name.

    This view requires the user to be authenticated, and `only allows staff` users to perform the listing.
    `Non-staff` users receive a `401 Unauthorized` response.

    Attributes:
        - `permission_classes (list)`: A list of permission classes required to access this view.
                In this case, it contains a single `IsAuthenticated` class.
        - `serializer_class`: The serializer class used to convert model instances to JSON.
                In this case, it is `CandidatesSerializers`.
        - `queryset`: The queryset used to fetch the data from the database.
                In this case, it is `User.objects.all()`, which returns all users in the database.
        - `filter_backends`: A list of filter backends used to filter the queryset.
                In this case, it contains a single SearchFilter backend.
        - `search_fields`: A list of model fields that can be used for text search.
                In this case, it contains the `'name'` field.

    Methods:
        - `list(request)`: The main method of this view, which returns a list of job seekers filtered by name.

    Returns:
        - A Response object with a list of job seekers, or an error message if the user is not authorized.
    """

    serializer_class = CandidatesSerializers
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter, django_filters.DjangoFilterBackend]
    filterset_class = UsersFilter
    search_fields = ['name', 'email']
    pagination_class = CustomPagination

    def list(self, request):
        context = dict()
        if self.request.user.is_staff:
            queryset = self.filter_queryset(self.get_queryset().filter(Q(role="job_seeker") | Q(role="vendor")))
            action = request.GET.get('action', None)
            if action == 'download':
                directory_path = create_directory()
                file_name = '{0}/{1}'.format(directory_path, 'candidate.csv')
                with open(file_name, mode='w') as data_file:
                    file_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    file_writer.writerow(
                        ["Number", "Role", "Name", "Email", "Mobile Number"]
                    )
                    for counter, rows in enumerate(queryset):
                        mobile_number = "None"
                        if rows.country_code:
                            mobile_number = str(rows.country_code) + str(rows.mobile_number)
                        file_writer.writerow(
                            [
                                str(counter + 1), str(rows.role), str(rows.name), str(rows.email), mobile_number
                            ]
                        )
                return response.Response(
                    data={"url": "/" + file_name},
                    status=status.HTTP_200_OK
                )
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True, context=context)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True, context=context)
            return response.Response(serializer.data)
        else:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
            )


class EmployerListView(generics.ListAPIView):
    """
    API view for listing employers by name.

    This view requires the user to be authenticated, and `only allows staff` users to perform the listing.
    `Non-staff` users receive a `401 Unauthorized` response.

    Attributes:
        - `permission_classes (list)`: A list of permission classes required to access this view.
                In this case, it contains a single `IsAuthenticated` class.
        - `serializer_class`: The serializer class used to convert model instances to JSON.
                In this case, it is `CandidatesSerializers`.
        - `queryset`: The queryset used to fetch the data from the database.
                In this case, it is `User.objects.all()`, which returns all users in the database.
        - `filter_backends`: A list of filter backends used to filter the queryset.
                In this case, it contains a single SearchFilter backend.
        - `search_fields`: A list of model fields that can be used for text search.
                In this case, it contains the `'name'` field.

    Methods:
        - `list(request)`: The main method of this view, which returns a list of employers filtered by name.

    Returns:
        - A Response object with a list of employers, or an error message if the user is not authorized.
    """

    serializer_class = CandidatesSerializers
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter, django_filters.DjangoFilterBackend]
    filterset_class = UsersFilter
    search_fields = ['name']
    pagination_class = CustomPagination

    def list(self, request):
        context = dict()
        if self.request.user.is_staff:
            queryset = self.filter_queryset(self.get_queryset().filter(role="employer"))
            action = request.GET.get('action', None)
            if action == 'download':
                directory_path = create_directory()
                file_name = '{0}/{1}'.format(directory_path, 'employers.csv')
                with open(file_name, mode='w') as data_file:
                    file_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    file_writer.writerow(
                        ["Number", "Name", "Email", "Mobile Number"]
                    )
                    for counter, rows in enumerate(queryset):
                        mobile_number = "None"
                        if rows.country_code:
                            mobile_number = str(rows.country_code) + str(rows.mobile_number)
                        file_writer.writerow(
                            [
                                str(counter + 1), str(rows.name), str(rows.email), mobile_number
                            ]
                        )
                return response.Response(
                    data={"url": "/" + file_name},
                    status=status.HTTP_200_OK
                )
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True, context=context)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True, context=context)
            return response.Response(serializer.data)
        else:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
            )

    def put(self, request, employerId, action):
        """
        Updates the verification status of an employer profile.

        Args:
            request (HttpRequest): The HTTP request object.
            employerId (int): The ID of the employer profile.
            action (str): The action to perform ('verify' or 'unverify').

        Returns:
            Response: The response object containing the updated context and status.

        Raises:
            NotFound: If the employer profile with the specified ID doesn't exist.
            BadRequest: If any other exception occurs during the process.
        """
        if not self.request.user.is_staff:
            context = {'message': "You do not have permission to perform this action."}
            return response.Response(data=context, status=status.HTTP_401_UNAUTHORIZED)

        try:
            employer_instance = EmployerProfile.objects.get(user_id=employerId)
        except EmployerProfile.DoesNotExist:
            return response.Response(data={"employerId": "Does Not Exist"}, status=status.HTTP_404_NOT_FOUND)

        context = {'message': ''}
        if action == 'verify':
            if employer_instance.is_verified:
                context['message'] = "Employer is already verified"
            else:
                employer_instance.is_verified = True
                employer_instance.save()
                context['message'] = "Employer verified."
        elif action == 'unverify':
            if not employer_instance.is_verified:
                context['message'] = "Employer is not verified"
            else:
                employer_instance.is_verified = False
                employer_instance.save()
                context['message'] = "Employer unverified."
        else:
            context['message'] = "Invalid action"

        return response.Response(data=context, status=status.HTTP_200_OK)


class JobsListView(generics.ListAPIView):
    """
    API view for listing jobs by name.

    This view requires the user to be authenticated, and `only allows staff` users to perform the listing.
    `Non-staff` users receive a `401 Unauthorized` response.

    Attributes:
        - `permission_classes (list)`: A list of permission classes required to access this view.
                In this case, it contains a single `IsAuthenticated` class.
        - `serializer_class`: The serializer class used to convert model instances to JSON.
                In this case, it is `JobListSerializers`.
        - `queryset`: The queryset used to fetch the data from the database.
                In this case, it is `JobDetails.objects.all()`, which returns all jobs in the database.
        - `filter_backends`: A list of filter backends used to filter the queryset.
                In this case, it contains a single SearchFilter backend.
        - `search_fields`: A list of model fields that can be used for text search.
                In this case, it contains the `'title'` field.

    Methods:
        - `list(request)`: The main method of this view, which returns a list of jobs filtered by title.

    Returns:
        - A Response object with a list of jobs, or an error message if the user is not authorized.
    """

    serializer_class = JobListSerializers
    permission_classes = [permissions.IsAuthenticated]
    queryset = JobDetails.objects.all().order_by('-created')
    filter_backends = [filters.SearchFilter, django_filters.DjangoFilterBackend]
    filterset_class = JobDetailsFilter
    search_fields = [
        'title', 'description',
        'skill__title', 'highest_education__title',
        'job_category__title', 'country__title',
        'city__title'
    ]
    pagination_class = CustomPagination

    def list(self, request):
        """
        Retrieve a list of jobs with optional download capability for staff users.

        This view returns a paginated list of jobs based on the queryset defined in `get_queryset()`. For staff users,
        the view provides an option to download the job data as a CSV file. Non-staff users will receive an unauthorized
        response.

        Parameters:
            - `request` : rest_framework.request.Request
                The HTTP request object.

        Returns:
            - `Response` : rest_framework.response.Response
                The HTTP response object containing the paginated job data or a download URL for staff users.

        Raises:
            - `PermissionDenied` : rest_framework.exceptions.PermissionDenied
                If the user does not have staff status and attempts to download job data.

        IOError : builtins.IOError
            If an error occurs during file I/O while creating the CSV file for download.
        """

        context = dict()
        if self.request.user.is_staff:
            queryset = self.filter_queryset(self.get_queryset())
            action = request.GET.get('action', None)
            if action == 'download':
                directory_path = create_directory()
                file_name = '{0}/{1}'.format(directory_path, 'jobs.csv')
                with open(file_name, mode='w') as data_file:
                    file_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    file_writer.writerow(
                        ["Number", "Job ID", "Job Title", "Company", "Location"])
                    for counter, rows in enumerate(queryset):
                        location = "None"
                        if rows.city:
                            location = str(rows.city) + ", " + str(rows.country)
                        file_writer.writerow(
                            [
                                str(counter + 1), str(rows.job_id), str(rows.title),
                                str(rows.user.name), location
                            ]
                        )
                return response.Response(
                    data={"url": "/" + file_name},
                    status=status.HTTP_200_OK
                )
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True, context=context)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True, context=context)
            return response.Response(serializer.data)
        else:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
            )

    def delete(self, request, jobId):
        """
        Deletes a Job object with the given ID if the authenticated user is a admin.
        Args:
            request: A DRF request object.
            jobId: An integer representing the ID of the Job to be deleted.
        Returns:
            A DRF response object with a success or error message and appropriate status code.
        """
        context = dict()
        if self.request.user.is_staff:
            try:
                JobDetails.objects.get(id=jobId).delete()
                context['message'] = "Deleted Successfully"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
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
        else:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
            )

    def patch(self, request, jobId):
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
        if self.request.user.is_staff:
            try:
                jobs_instance = JobDetails.objects.get(id=jobId)
                if jobs_instance.status == "inactive":
                    jobs_instance.status = "active"
                    context['message'] = "This job is active"
                else:
                    jobs_instance.status = "inactive"
                    context['message'] = "This job is inactive"
                jobs_instance.save()
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
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
        else:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
            )


class UsersCountView(generics.GenericAPIView):
    """
    A view that returns the number of users registered in the system if the user has staff level permissions,
    and returns an error message otherwise.

    Attributes:
        - `permission_classes (list)`: A list of permission classes that control access to this view.
        - `serializer_class (class)`: The serializer class used to convert data to/from JSON format.

    Methods:
        - `get(self, request)`: Retrieves the number of users registered in the system and returns a response.
                                If the user does not have staff level permissions, an error message is returned.

    Returns:
        - `response.Response`: The response containing the serialized data or error message.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = UserCountSerializers

    def get(self, request):
        context = dict()
        if self.request.user.is_staff:
            try:
                queryset = User.objects.all()
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
        else:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
            )


class UserView(generics.GenericAPIView):
    """
    A class-based view that provides generic CRUD (Update, Delete) operations for User instances.

    This view requires authentication to perform any CRUD operation, as specified by the permission_classes attribute.

    Attributes:
        - permission_classes: A list of permission classes that defines the permission policy for this view.
                            In this case, the IsAuthenticated permission class is used to require authentication for all requests.
    """

    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, userId):
        """
        Deletes a User object with the given ID if the authenticated user is a admin.
        Args:
            request: A DRF request object.
            userId: An integer representing the ID of the User to be deleted.
        Returns:
            A DRF response object with a success or error message and appropriate status code.
        """
        context = dict()
        if self.request.user.is_staff:
            try:
                User.objects.get(id=userId)
                User.objects.filter(id=userId).delete()
                context['message'] = "Deleted Successfully"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                return response.Response(
                    data={"userId": "Does Not Exist"},
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

    def patch(self, request, userId):
        """
        View function for `updating the status` of a user instance.

        Args:
            - `request`: Request object containing metadata about the current request.
            - `userId`: Integer representing the ID of the user instance to be updated.

        Returns:
            Response object containing data about the updated user instance, along with an HTTP status code.

        Raises:
            - `Http404`: If the user instance with the given `userId does not exist`.
        """

        context = dict()
        if self.request.user.is_staff:
            try:
                user_instance = User.objects.get(id=userId)
                if not user_instance.is_active:
                    user_instance.is_active = True
                    context['message'] = "This user is active"
                else:
                    user_instance.is_active = False
                    context['message'] = "This user is inactive"
                user_instance.save()
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                return response.Response(
                    data={"userId": "Does Not Exist"},
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


class JobsRevertView(generics.GenericAPIView):
    """
    The `JobsRevertView` class is a generic view that allows staff users to restore a removed job by sending a PATCH
    request to the API with the jobId as a parameter.

    Parameters:
        - `request`: The HTTP request object
        - `jobId`: The ID of the job to be restored

    Returns:
        - A response object with a success or error message and an HTTP status code.

    Raises:
        - `JobDetails.DoesNotExist`: If the job with the given jobId does not exist in the database.
        - `Exception`: If an unexpected error occurs.

    Permissions:
        - The user must be authenticated and have staff status to perform this action.
    """

    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, jobId):

        context = dict()
        if self.request.user.is_staff:
            try:
                JobDetails.all_objects.get(id=jobId, is_removed=True)
                JobDetails.all_objects.filter(id=jobId, is_removed=True).update(is_removed=False)
                context['message'] = "Job restored successfully"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
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
        else:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
            )


class DashboardView(generics.GenericAPIView):
    """
    `DashboardView` is a generic API view that returns `counts` of `active jobs` and `employers` based on specified
    `period` or `start and end dates`. The view accepts `GET requests` and requires the user to have
    `staff permissions`.

    Attributes:
        - `permission_classes (list)`: A list of permission classes that the user must have in order to access this
                                        view.
        - `serializer_class (DashboardCountSerializers)`: The serializer class used to serialize the response data.

    Methods:
        - `get(request)`: A method that handles GET requests and returns `counts of active jobs and employers` based on
                            specified `period` or `start and end dates`.

    Example usage:
    To access this view, make a GET request with the following parameters:
        - `period (optional)`: a string representing the `time period` for which to retrieve counts. Can be one of
                                '`this week`', '`last week`', '`this month`', '`last month`', '`this year`', or
                                '`last year`'.
        - `start-date (optional)`: a string representing the `start date` for which to retrieve counts. Must be in
                                    '`YYYY-MM-DD`' format.
        - `end-date (optional)`: a string representing the `end date` for which to retrieve counts. Must be in
                                    '`YYYY-MM-DD`' format.
        If the user is not authorized to access this view, a 401 Unauthorized response will be returned. If the request
        is invalid or there is an error retrieving the counts, a 400 Bad Request response will be returned with a
        message describing the error.

    """

    permission_classes = [permissions.AllowAny]
    serializer_class = DashboardCountSerializers

    def get(self, request):
        response_context = dict()
        user_context = dict()
        if self.request.user.is_staff:
            try:
                if 'period' in self.request.GET and 'start-date' in self.request.GET:
                    response_context['message'] = "Please select one eighter 'period' or 'start and end dates'."
                    return response.Response(
                        data=response_context,
                        status=status.HTTP_400_BAD_REQUEST
                    )
                period = self.request.GET.get('period', None)
                start_date = self.request.GET.get('start-date', date.today())
                end_date = self.request.GET.get('end-date', date.today())
                if period == "this week":
                    start_date = start_date - timedelta(days=start_date.weekday())
                elif period == "last week":
                    last_week = date.today() + timedelta(days=-2)
                    start_date = last_week - timedelta(days=last_week.weekday())
                    end_date = start_date + timedelta(days=6)
                elif period == "this month":
                    start_date = date(start_date.year, start_date.month, 1)
                elif period == "last month":
                    start_date = date(start_date.year, start_date.month, 1)
                    end_date = start_date + timedelta(days=-1)
                    start_date = date(end_date.year, end_date.month, 1)
                elif period == "this year":
                    start_date = date(start_date.year, 1, 1)
                elif period == "last year":
                    start_date = date(start_date.year, 1, 1)
                    end_date = start_date + timedelta(days=-1)
                    start_date = date(end_date.year, 1, 1)
                context = {
                    "start_date": start_date,
                    "end_date": end_date
                }
                queryset = User.objects.all()
                serializer = self.serializer_class(queryset, context=context)
                return response.Response(
                    data=serializer.data,
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                response_context['message'] = str(e)
                return response.Response(
                    data=response_context,
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            response_context['message'] = "You do not have permission to perform this action."
            return response.Response(
                data=response_context,
                status=status.HTTP_401_UNAUTHORIZED
            )


class TenderCategoryView(generics.ListAPIView):
    """
    A view for displaying a list of tender categories .

    Attributes:
        - permission_classes ([permissions.IsAuthenticated]): List of permission classes that the view requires. In this
            case, only authenticated users are allowed to access the view.

        - serializer_class (TenderCategorySerializers): The serializer class used for data validation and serialization.

        - queryset (QuerySet): The queryset that the view should use to retrieve the countries. By default, it is set
            to retrieve all countries using `TenderCategory.objects.all()`.

        - filter_backends ([filters.SearchFilter]): List of filter backends to use for filtering the queryset. In this
            case, only `SearchFilter` is used.

        - search_fields (list): List of fields to search for in the queryset. In this case, the field is "title".

    """

    permission_classes = [permissions.AllowAny]
    serializer_class = TenderCategorySerializers
    queryset = TenderCategory.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    pagination_class = CustomPagination

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def post(self, request):
        """
        Handle POST request to create a new tender category.
        The request must contain valid data for the tender category to be created.

        Only users with `is_staff` attribute set to True are authorized to create a tender category.

        Returns:
            - HTTP 201 CREATED with added tender category data (id, title) if the tender category is created successfully.
            - HTTP 400 BAD REQUEST with error message if data validation fails.
            - HTTP 401 UNAUTHORIZED with a message "You do not have permission to perform this action." if the user is
            not authorized.

        Raises:
            Exception: If an unexpected error occurs during the request handling.
        """
        context = dict()
        serializer = self.serializer_class(data=request.data)
        try:
            if self.request.user.is_staff:
                serializer.is_valid(raise_exception=True)
                if TenderCategory.all_objects.filter(title__iexact=serializer.validated_data['title'],
                                                     is_removed=True).exists():
                    TenderCategory.all_objects.filter(title__iexact=serializer.validated_data['title'],
                                                      is_removed=True).update(
                        is_removed=False)
                else:
                    serializer.save()
                return response.Response(
                    data=serializer.data,
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

    def delete(self, request, tenderCategoryId):
        """
        Deletes an TenderCategory object with the given ID if the authenticated user is a job seeker and owns the
        TenderCategory.
        Args:
            request: A DRF request object.
            educationId: An integer representing the ID of the TenderCategory to be deleted.
        Returns:
            A DRF response object with a success or error message and appropriate status code.
        """
        context = dict()
        if self.request.user.is_staff:
            try:
                TenderCategory.objects.get(id=tenderCategoryId).delete()
                context['message'] = "Deleted Successfully"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except TenderCategory.DoesNotExist:
                return response.Response(
                    data={"tenderCategoryId": "Does Not Exist"},
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

    def put(self, request, tenderCategoryId):
        """
        Update an `TenderCategory` instance with the provided data.

        Args:
            - `request (django.http.request.Request)`: The HTTP request object.
            - `tenderCategoryId (int)`: The ID of the `TenderCategory` instance to update.

        Returns:
            - `django.http.response.Response`: An HTTP response object containing the updated data
            and appropriate status code.

        Raises:
            - `serializers.ValidationError`: If the provided data is invalid.
            - `TenderCategory.DoesNotExist`: If the TenderCategory instance with the given ID does not exist.
            - `Exception`: If any other error occurs during the update process.
        """

        context = dict()
        try:
            tender_category_instance = TenderCategory.all_objects.get(id=tenderCategoryId)
            serializer = self.serializer_class(data=request.data, instance=tender_category_instance, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                if serializer.update(tender_category_instance, serializer.validated_data):
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
        except TenderCategory.DoesNotExist:
            return response.Response(
                data={"tenderCategoryId": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["message"] = e
            return response.Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
            )


def create_directory():
    """
    Create a directory for storing CSV files in the 'media' directory with the current date as the subdirectory name.

    Returns:
    - `directory_url` : str
        The URL of the created directory.

    Raises:
    - `OSError`:
        If directory creation fails due to permission issues or other reasons.
    """

    directory_url = '{0}/{1}/{2}'.format('media', 'csv_file', date.today())
    directory_url_path_check = pathlib.Path(directory_url)
    if directory_url_path_check.exists():
        directory_url = directory_url
    else:
        os.makedirs(directory_url)
        directory_url = directory_url
    return directory_url


class UploadCountryView(generics.GenericAPIView):
    """
    API view for uploading country data from a CSV file.

    - This view handles the HTTP POST request for uploading country data from a CSV file.
    - The uploaded CSV file is read, parsed, and the data is saved to the AllCountry model in the database.
    - The user must be authenticated and have staff permissions to access this view.

    Attributes:
        - `permission_classes (list)`: List of permission classes required to access this view.
                Only authenticated users with staff permissions are allowed.
    
    Methods:
        - `post(request)`: Handles the POST request for uploading country data.
                Reads and parses the uploaded CSV file, and saves the data to the AllCountry model.
                Returns a response with a success message and HTTP 201 status code if successful, or an error message
                and HTTP 401 status code if the user is not authenticated or does not have staff permissions.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Handles the POST request for uploading country data from a CSV file.

        Args:
            - `request (HttpRequest)`: The HTTP request object.

        Returns:
            - `Response`: A response object containing a success message and HTTP 201 status code if the country data
                        is uploaded successfully, or an error message and HTTP 401 status code if the user is not
                        authenticated or does not have staff permissions.
        """

        context = dict()
        if self.request.user.is_staff:
            csv_file = request.FILES.get('csv_file', None)
            if csv_file:
                data_set = csv_file.read().decode('UTF-8')
                io_string = io.StringIO(data_set)
                get_data = csv.reader(io_string)
                for row in get_data:
                    if row[0].isdigit():
                        if AllCountry.objects.filter(id=row[0]).exists():
                            AllCountry.objects.filter(id=row[0]).update(
                                title=row[1], iso3=row[2], iso2=row[3],
                                phone_code=row[4], currency=row[5]
                            )
                        else:
                            AllCountry.objects.create(
                                id=row[0], title=row[1], iso3=row[2], iso2=row[3],
                                phone_code=row[4], currency=row[5]
                            )
            context['message'] = "Countries added successfully"
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


class UploadCityView(generics.GenericAPIView):
    """
    API view for `uploading cities` data from a CSV file.

    Attributes:
        - `permission_classes (list)`: The list of permission classes that the view requires.

    Methods:
        - `post(request)`: Handles HTTP POST requests to upload cities data from a `CSV file`.

    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Handle HTTP POST requests to `upload cities data from a CSV file`.

        Args:
            - `request (HttpRequest)`: The HTTP request object.

        Returns:
            - A Response object with a JSON-encoded representation of the response data.

        Raises:
            - N/A

        """

        context = dict()
        if self.request.user.is_staff:
            csv_file = request.FILES.get('csv_file', None)
            if csv_file:
                data_set = csv_file.read().decode('UTF-8')
                io_string = io.StringIO(data_set)
                get_data = csv.reader(io_string)
                for row in get_data:
                    if row[0].isdigit():
                        if AllCity.objects.filter(id=row[0]).exists():
                            if AllCountry.objects.filter(id=row[2]).exists():
                                country = AllCountry.objects.get(id=row[2])
                                AllCity.objects.filter(id=row[0]).update(
                                    title=row[1], country=country
                                )
                        else:
                            if AllCountry.objects.filter(id=row[2]).exists():
                                country = AllCountry.objects.get(id=row[2])
                                AllCity.objects.create(
                                    id=row[0], title=row[1], country=country
                                )
            context['message'] = "Cities added successfully"
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


class JobSubCategoryView(generics.ListAPIView):
    """
    A view for displaying a list of job sub categories.

    Attributes:
        - permission_classes ([permissions.IsAuthenticated]): List of permission classes that the view requires. In this
            case, only authenticated users are allowed to access the view.

        - serializer_class (JobSubCategorySerializers): The serializer class used for data validation and serialization.

        - queryset (QuerySet): The queryset that the view should use to retrieve the countries. By default, it is set
            to retrieve all countries using `JobSubCategory.objects.all()`.

        - filter_backends ([filters.SearchFilter]): List of filter backends to use for filtering the queryset. In this
            case, only `SearchFilter` is used.

        - search_fields (list): List of fields to search for in the queryset. In this case, the field is "title".

    """

    permission_classes = [permissions.AllowAny]
    serializer_class = GetJobSubCategorySerializers
    queryset = JobSubCategory.objects.filter(category__is_removed=False).order_by("category")
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'category__title']
    pagination_class = CustomPagination

    def list(self, request):
        category_id = request.GET.get('categoryId', None)
        if category_id:
            queryset = self.filter_queryset(self.get_queryset().filter(category_id=category_id))
        else:
            queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def post(self, request):
        """
        Handle POST request to create a new job sub category.
        The request must contain valid data for the job sub category to be created.

        Only users with `is_staff` attribute set to True are authorized to create a job sub category.

        Returns:
            - HTTP 201 CREATED with a message "JobSubCategory added successfully" if the job sub category is created
            successfully.
            - HTTP 400 BAD REQUEST with error message if data validation fails.
            - HTTP 401 UNAUTHORIZED with a message "You do not have permission to perform this action." if the user is
            not authorized.

        Raises:
            Exception: If an unexpected error occurs during the request handling.
        """
        context = dict()
        serializer = JobSubCategorySerializers(data=request.data)
        try:
            if self.request.user.is_staff:
                serializer.is_valid(raise_exception=True)
                if JobSubCategory.all_objects.filter(title__iexact=serializer.validated_data['title'],
                                                     is_removed=True).exists():
                    JobSubCategory.all_objects.filter(title__iexact=serializer.validated_data['title'],
                                                      is_removed=True).update(
                        is_removed=False)
                else:
                    serializer.save()
                context["data"] = serializer.data
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

    def delete(self, request, jobSubCategoryId):
        """
        Deletes an JobSubCategory object with the given ID if the authenticated user is a job seeker and owns the
        JobSubCategory.
        Args:
            request: A DRF request object.
            educationId: An integer representing the ID of the JobSubCategory to be deleted.
        Returns:
            A DRF response object with a success or error message and appropriate status code.
        """
        context = dict()
        if self.request.user.is_staff:
            try:
                JobSubCategory.objects.get(id=jobSubCategoryId).delete()
                context['message'] = "Deleted Successfully"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except JobSubCategory.DoesNotExist:
                return response.Response(
                    data={"jobSubCategoryId": "Does Not Exist"},
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

    def put(self, request, jobSubCategoryId):
        """
        Update an `JobSubCategory` instance with the provided data.

        Args:
            - `request (django.http.request.Request)`: The HTTP request object.
            - `jobSubCategoryId (int)`: The ID of the `JobSubCategory` instance to update.

        Returns:
            - `django.http.response.Response`: An HTTP response object containing the updated data
            and appropriate status code.

        Raises:
            - `serializers.ValidationError`: If the provided data is invalid.
            - `JobSubCategory.DoesNotExist`: If the JobSubCategory instance with the given ID does not exist.
            - `Exception`: If any other error occurs during the update process.
        """

        context = dict()
        try:
            job_sub_category_instance = JobSubCategory.all_objects.get(id=jobSubCategoryId)
            serializer = JobSubCategorySerializers(data=request.data, instance=job_sub_category_instance, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                if serializer.update(job_sub_category_instance, serializer.validated_data):
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
        except JobSubCategory.DoesNotExist:
            return response.Response(
                data={"jobSubCategoryId": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["message"] = e
            return response.Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
            )


class WorldCountryView(generics.ListAPIView):
    """
    A view that returns a list of all countries in the world.

    This view supports searching for countries by title using the `title` query parameter.

    Attributes:
    - `permission_classes` : list of classes
        - The list of permission classes that the view requires.
        - In this case, any user is allowed to access the view.
    - `serializer_class` : Serializer class
        - The serializer class that will be used to serialize the country data returned by the view. In this 
        case, the `AllCountrySerializers` serializer will be used.
    - `queryset` : QuerySet
        - The queryset of all countries that will be used by the view.
        - In this case, the `AllCountry` model's all objects will be used.
    - `filter_backends` : list of classes
        - The list of filter backend classes that the view will use to filter
        the queryset. In this case, the `SearchFilter` backend will be used.
    - `search_fields` : list of strings
        - The list of fields that will be used for searching countries by title.
        - In this case, only the `title` field will be searched with the "^" prefix, which means that 
        the search is case-insensitive and searches for the start of the field value.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = AllCountrySerializers
    queryset = AllCountry.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['^title']


class WorldCityView(generics.ListAPIView):
    """
    API view for retrieving a list of cities from the database.

    Attributes:
        - `permission_classes (list)`: The list of permission classes that the view requires.
        - `serializer_class (class)`: The serializer class to use for the view.
        - `queryset (QuerySet)`: The queryset to use for the view.
        - `filter_backends (list)`: The list of filter backend classes to use for the view.
        - `search_fields (list)`: The list of model fields to search against for the search filter.
        - `pagination_class (class)`: The pagination class to use for the view.

    Methods:
        - `list(request)`: Handles HTTP GET requests to retrieve a list of cities from the database.

    """

    permission_classes = [permissions.AllowAny]
    serializer_class = AllCitySerializers
    queryset = AllCity.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['^title']
    pagination_class = CustomPagination

    def list(self, request):
        """
        Handle HTTP GET requests to retrieve a list of cities from the database.

        Args:
            - `request (HttpRequest)`: The HTTP request object.

        Returns:
            - A Response object with a JSON-encoded representation of the response data.

        Raises:
            - N/A

        """

        country_name = request.GET.get('countryName', None)
        if country_name:
            queryset = self.filter_queryset(self.get_queryset().filter(country__title__iexact=country_name))
        else:
            queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)


class ChoiceView(generics.ListAPIView):
    """
    A view for displaying a list of choices .

    Attributes:
        - permission_classes ([permissions.IsAuthenticated]): List of permission classes that the view requires. In this
            case, only authenticated users are allowed to access the view.

        - serializer_class (ChoiceSerializers): The serializer class used for data validation and serialization.

        - queryset (QuerySet): The queryset that the view should use to retrieve the countries. By default, it is set
            to retrieve all countries using `Choice.objects.all()`.

        - filter_backends ([filters.SearchFilter]): List of filter backends to use for filtering the queryset. In this
            case, only `SearchFilter` is used.

        - search_fields (list): List of fields to search for in the queryset. In this case, the field is "title".

    """

    permission_classes = [permissions.AllowAny]
    serializer_class = ChoiceSerializers
    queryset = Choice.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    pagination_class = CustomPagination

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def post(self, request):
        """
        Handle POST request to create a new choice.
        The request must contain valid data for the choice to be created.

        Only users with `is_staff` attribute set to True are authorized to create a choice.

        Returns:
            - HTTP 201 CREATED with added choice data (id, title) if the choice is created successfully.
            - HTTP 400 BAD REQUEST with error message if data validation fails.
            - HTTP 401 UNAUTHORIZED with a message "You do not have permission to perform this action." if the user is
            not authorized.

        Raises:
            Exception: If an unexpected error occurs during the request handling.
        """
        context = dict()
        serializer = self.serializer_class(data=request.data)
        try:
            if self.request.user.is_staff:
                serializer.is_valid(raise_exception=True)
                if Choice.all_objects.filter(title__iexact=serializer.validated_data['title'], is_removed=True).exists():
                    Choice.all_objects.filter(title__iexact=serializer.validated_data['title'], is_removed=True).update(
                        is_removed=False)
                else:
                    serializer.save()
                context["data"] = serializer.data
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

    def delete(self, request, sectorId):
        """
        Deletes an Choice object with the given ID if the authenticated user is a job seeker and owns the
        Choice.
        Args:
            request: A DRF request object.
            educationId: An integer representing the ID of the Choice to be deleted.
        Returns:
            A DRF response object with a success or error message and appropriate status code.
        """
        context = dict()
        if self.request.user.is_staff:
            try:
                Choice.objects.get(id=sectorId).delete()
                context['message'] = "Deleted Successfully"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except Choice.DoesNotExist:
                return response.Response(
                    data={"choice": "Does Not Exist"},
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

    def put(self, request, sectorId):
        """
        Update a `Choice` instance with the provided data.

        Args:
            - `request (django.http.request.Request)`: The HTTP request object.
            - `sectorId (int)`: The ID of the `Choice` instance to update.

        Returns:
            - `django.http.response.Response`: An HTTP response object containing the updated data
            and appropriate status code.

        Raises:
            - `serializers.ValidationError`: If the provided data is invalid.
            - `Choice.DoesNotExist`: If the Choice instance with the given ID does not exist.
            - `Exception`: If any other error occurs during the update process.

        """

        context = dict()
        try:
            choice_instance = Choice.all_objects.get(id=sectorId)
            serializer = self.serializer_class(data=request.data, instance=choice_instance, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                if serializer.update(choice_instance, serializer.validated_data):
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
        except Choice.DoesNotExist:
            return response.Response(
                data={"sectorId": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["message"] = e
            return response.Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
            )


class OpportunityTypeView(generics.ListAPIView):
    """
    A view for displaying a list of opportunity types .

    Attributes:
        - permission_classes ([permissions.IsAuthenticated]): List of permission classes that the view requires. In this
            case, only authenticated users are allowed to access the view.

        - serializer_class (OpportunityTypeSerializers): The serializer class used for data validation and serialization.

        - queryset (QuerySet): The queryset that the view should use to retrieve the countries. By default, it is set
            to retrieve all countries using `OpportunityType.objects.all()`.

        - filter_backends ([filters.SearchFilter]): List of filter backends to use for filtering the queryset. In this
            case, only `SearchFilter` is used.

        - search_fields (list): List of fields to search for in the queryset. In this case, the field is "title".

    """

    permission_classes = [permissions.AllowAny]
    serializer_class = OpportunityTypeSerializers
    queryset = OpportunityType.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    pagination_class = CustomPagination

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def post(self, request):
        """
        Handle POST request to create a new opportunity type.
        The request must contain valid data for the opportunity type to be created.

        Only users with `is_staff` attribute set to True are authorized to create a opportunity type.

        Returns:
            - HTTP 201 CREATED with added opportunity type data (id, title) if the opportunity type is created successfully.
            - HTTP 400 BAD REQUEST with error message if data validation fails.
            - HTTP 401 UNAUTHORIZED with a message "You do not have permission to perform this action." if the user is
            not authorized.

        Raises:
            Exception: If an unexpected error occurs during the request handling.
        """
        context = dict()
        serializer = self.serializer_class(data=request.data)
        try:
            if self.request.user.is_staff:
                serializer.is_valid(raise_exception=True)
                if OpportunityType.all_objects.filter(title__iexact=serializer.validated_data['title'], is_removed=True).exists():
                    OpportunityType.all_objects.filter(title__iexact=serializer.validated_data['title'], is_removed=True).update(
                        is_removed=False)
                else:
                    serializer.save()
                context["data"] = serializer.data
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

    def delete(self, request, opportunityId):
        """
        Deletes an OpportunityType object with the given ID if the authenticated user is a job seeker and owns the
        OpportunityType.
        Args:
            request: A DRF request object.
            educationId: An integer representing the ID of the OpportunityType to be deleted.
        Returns:
            A DRF response object with a success or error message and appropriate status code.
        """
        context = dict()
        if self.request.user.is_staff:
            try:
                OpportunityType.objects.get(id=opportunityId).delete()
                context['message'] = "Deleted Successfully"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except OpportunityType.DoesNotExist:
                return response.Response(
                    data={"OpportunityType": "Does Not Exist"},
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

    def put(self, request, opportunityId):
        """
        Update a `OpportunityType` instance with the provided data.

        Args:
            - `request (django.http.request.Request)`: The HTTP request object.
            - `opportunityId (int)`: The ID of the `OpportunityType` instance to update.

        Returns:
            - `django.http.response.Response`: An HTTP response object containing the updated data
            and appropriate status code.

        Raises:
            - `serializers.ValidationError`: If the provided data is invalid.
            - `OpportunityType.DoesNotExist`: If the OpportunityType instance with the given ID does not exist.
            - `Exception`: If any other error occurs during the update process.

        """

        context = dict()
        try:
            opportunity_instance = OpportunityType.all_objects.get(id=opportunityId)
            serializer = self.serializer_class(data=request.data, instance=opportunity_instance, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                if serializer.update(opportunity_instance, serializer.validated_data):
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
        except OpportunityType.DoesNotExist:
            return response.Response(
                data={"opportunityId": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["message"] = e
            return response.Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
            )


class TenderListView(generics.ListAPIView):
    """
    API view for listing tenders by name.

    This view requires the user to be authenticated, and `only allows staff` users to perform the listing.
    `Non-staff` users receive a `401 Unauthorized` response.

    Attributes:
        - `permission_classes (list)`: A list of permission classes required to access this view.
                In this case, it contains a single `IsAuthenticated` class.
        - `serializer_class`: The serializer class used to convert model instances to JSON.
                In this case, it is `TenderListSerializers`.
        - `queryset`: The queryset used to fetch the data from the database.
                In this case, it is `TenderDetails.objects.all()`, which returns all tenders in the database.
        - `filter_backends`: A list of filter backends used to filter the queryset.
                In this case, it contains a single SearchFilter backend.
        - `search_fields`: A list of model fields that can be used for text search.
                In this case, it contains the `'title'` field.

    Methods:
        - `list(request)`: The main method of this view, which returns a list of tenders filtered by title.

    Returns:
        - A Response object with a list of tenders, or an error message if the user is not authorized.
    """

    serializer_class = TenderListSerializers
    permission_classes = [permissions.IsAuthenticated]
    queryset = TenderDetails.objects.all().order_by('-created')
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
        Retrieve a list of tenders with optional download capability for staff users.

        This view returns a paginated list of tenders based on the queryset defined in `get_queryset()`. For staff users,
        the view provides an option to download the tender data as a CSV file. Non-staff users will receive an unauthorized
        response.

        Parameters:
            - `request` : rest_framework.request.Request
                The HTTP request object.

        Returns:
            - `Response` : rest_framework.response.Response
                The HTTP response object containing the paginated tender data or a download URL for staff users.

        Raises:
            - `PermissionDenied` : rest_framework.exceptions.PermissionDenied
                If the user does not have staff status and attempts to download tender data.

        IOError : builtins.IOError
            If an error occurs during file I/O while creating the CSV file for download.
        """

        context = dict()
        if self.request.user.is_staff:
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
            action = request.GET.get('action', None)
            if action == 'download':
                directory_path = create_directory()
                file_name = '{0}/{1}'.format(directory_path, 'tenders.csv')
                with open(file_name, mode='w') as data_file:
                    file_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    file_writer.writerow(
                        ["Number", "Tender ID", "Tender Title", "Company", 
                         "Tag", "Tender Category", "Tender Type", "Sector", 
                         "Location"])
                    for counter, rows in enumerate(queryset):
                        location = "None"
                        tag = "None"
                        tender_category = "None"
                        tender_type = "None"
                        sector = "None"
                        if rows.city:
                            location = str(rows.city) + ", " + str(rows.country)                        
                        if rows.tag:
                            for data in rows.tag.all():
                                if tag != "None":
                                    tag = tag + ", " + str(data.title)
                                else:
                                    tag = str(data.title)                       
                        if rows.tender_category:
                            for data in rows.tender_category.all():
                                if tender_category != "None":
                                    tender_category = tender_category + ", " + str(data.title)
                                else:
                                    tender_category = str(data.title)                       
                        if rows.tender_type:
                            for data in rows.tender_type.all():
                                if tender_type != "None":
                                    tender_type = tender_type + ", " + str(data.title)
                                else:
                                    tender_type = str(data.title)
                        if rows.sector:
                            for data in rows.sector.all():
                                if sector != "None":
                                    sector = sector + ", " + str(data.title)
                                else:
                                    sector = str(data.title)
                        file_writer.writerow(
                            [
                                str(counter + 1), str(rows.job_id), str(rows.title),
                                str(rows.user.name), tag, tender_category, tender_type,
                                sector, location
                            ]
                        )
                return response.Response(
                    data={"url": "/" + file_name},
                    status=status.HTTP_200_OK
                )
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True, context=context)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True, context=context)
            return response.Response(serializer.data)
        else:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
            )

    def delete(self, request, tenderId):
        """
        Deletes a TenderDetails object with the given ID if the authenticated user is a admin.
        Args:
            request: A DRF request object.
            tenderId: An integer representing the ID of the TenderDetails to be deleted.
        Returns:
            A DRF response object with a success or error message and appropriate status code.
        """
        context = dict()
        if self.request.user.is_staff:
            try:
                TenderDetails.objects.get(id=tenderId).delete()
                context['message'] = "Deleted Successfully"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except TenderDetails.DoesNotExist:
                return response.Response(
                    data={"tenderId": "Does Not Exist"},
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

    def patch(self, request, tenderId):
        """
        View function for `updating the status` of a tender instance.

        Args:
            - `request`: Request object containing metadata about the current request.
            - `tenderId`: Integer representing the ID of the tender instance to be updated.

        Returns:
            Response object containing data about the updated tender instance, along with an HTTP status code.

        Raises:
            - `Http404`: If the tender instance with the given `tenderId does not exist`.
        """

        context = dict()
        if self.request.user.is_staff:
            try:
                tender_instance = TenderDetails.objects.get(id=tenderId)
                if tender_instance.status == "inactive":
                    tender_instance.status = "active"
                    context['message'] = "This tender is active"
                else:
                    tender_instance.status = "inactive"
                    context['message'] = "This tender is inactive"
                tender_instance.save()
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except TenderDetails.DoesNotExist:
                return response.Response(
                    data={"tenderId": "Does Not Exist"},
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


class TenderRevertView(generics.GenericAPIView):
    """
    The `TenderRevertView` class is a generic view that allows staff users to restore a removed tender by sending a PATCH
    request to the API with the tenderId as a parameter.

    Parameters:
        - `request`: The HTTP request object
        - `tenderId`: The ID of the tender to be restored

    Returns:
        - A response object with a success or error message and an HTTP status code.

    Raises:
        - `tenderDetails.DoesNotExist`: If the tender with the given tenderId does not exist in the database.
        - `Exception`: If an unexpected error occurs.

    Permissions:
        - The user must be authenticated and have staff status to perform this action.
    """

    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, tenderId):

        context = dict()
        if self.request.user.is_staff:
            try:
                TenderDetails.all_objects.get(id=tenderId, is_removed=True)
                TenderDetails.all_objects.filter(id=tenderId, is_removed=True).update(is_removed=False)
                context['message'] = "Job restored successfully"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except TenderDetails.DoesNotExist:
                return response.Response(
                    data={"tenderId": "Does Not Exist"},
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


class ResourcesView(generics.ListAPIView):
    """
    A view for displaying a list of resources.

    Attributes:
        - permission_classes ([permissions.IsAuthenticated]): List of permission classes that the view requires. In this
            case, only authenticated users are allowed to access the view.

        - serializer_class (ResourcesSerializers): The serializer class used for data validation and serialization.

        - queryset (QuerySet): The queryset that the view should use to retrieve the countries. By default, it is set
            to retrieve all countries using `ResourcesContent.objects.all()`.

        - filter_backends ([filters.SearchFilter]): List of filter backends to use for filtering the queryset. In this
            case, only `SearchFilter` is used.

        - search_fields (list): List of fields to search for in the queryset. In this case, the field is "title".

    """

    permission_classes = [permissions.AllowAny]
    serializer_class = ResourcesSerializers
    queryset = ResourcesContent.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    pagination_class = CustomPagination

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def post(self, request):
        """
        Handle POST request to create a new resource.
        The request must contain valid data for the resource to be created.

        Only users with `is_staff` attribute set to True are authorized to create a resource.

        Returns:
            - HTTP 201 CREATED with a message "Resources added successfully" if the resource is created
            successfully.
            - HTTP 400 BAD REQUEST with error message if data validation fails.
            - HTTP 401 UNAUTHORIZED with a message "You do not have permission to perform this action." if the user is
            not authorized.

        Raises:
            Exception: If an unexpected error occurs during the request handling.
        """
        context = dict()
        serializer = CreateResourcesSerializers(data=request.data)
        try:
            if self.request.user.is_staff:
                serializer.is_valid(raise_exception=True)
                if ResourcesContent.all_objects.filter(title__iexact=serializer.validated_data['title'],
                                                  is_removed=True).exists():
                    ResourcesContent.all_objects.filter(title__iexact=serializer.validated_data['title'],
                                                   is_removed=True).update(
                        is_removed=False)
                else:
                    serializer.save()
                context["data"] = serializer.data
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

    def delete(self, request, resourcesId):
        """
        Deletes an Resources object with the given ID if the authenticated user is a staff and owns the
        ResourcesContent.
        Args:
            request: A DRF request object.
            educationId: An integer representing the ID of the Resources to be deleted.
        Returns:
            A DRF response object with a success or error message and appropriate status code.
        """
        context = dict()
        if self.request.user.is_staff:
            try:
                ResourcesContent.objects.get(id=resourcesId).delete()
                context['message'] = "Deleted Successfully"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except ResourcesContent.DoesNotExist:
                return response.Response(
                    data={"resourcesId": "Does Not Exist"},
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

    def put(self, request, resourcesId):
        """
        Update an `ResourcesContent` instance with the provided data.

        Args:
            - `request (django.http.request.Request)`: The HTTP request object.
            - `resourcesId (int)`: The ID of the `ResourcesContent` instance to update.

        Returns:
            - `django.http.response.Response`: An HTTP response object containing the updated data
            and appropriate status code.

        Raises:
            - `serializers.ValidationError`: If the provided data is invalid.
            - `ResourcesContent.DoesNotExist`: If the ResourcesContent instance with the given ID does not exist.
            - `Exception`: If any other error occurs during the update process.
        """

        context = dict()
        try:
            resource_instance = ResourcesContent.all_objects.get(id=resourcesId)
            serializer = CreateResourcesSerializers(data=request.data, instance=resource_instance, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                if serializer.update(resource_instance, serializer.validated_data):
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
        except ResourcesContent.DoesNotExist:
            return response.Response(
                data={"resourcesId": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["message"] = e
            return response.Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
            )


class LinksView(generics.ListAPIView):
    """
    API view for retrieving a list of social URLs.

    - Permissions: Allow any user to access this view.
    - Serializer: SocialUrlSerializers
    - Queryset: All SocialUrl objects.
    - Filter backends: SearchFilter
    - Search fields: ['platform']
    - Pagination class: CustomPagination
    """
    
    permission_classes = [permissions.AllowAny]
    serializer_class = SocialUrlSerializers
    queryset = SocialUrl.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['platform']
    pagination_class = CustomPagination

    def list(self, request):
        """
        Retrieve a paginated list of objects.

        Args:
            - request: The HTTP request object.

        Returns:
            Response object containing serialized data of the paginated list.
        """
    
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def post(self, request):
        """
        Handles the HTTP POST request to create or update a social URL.

        Args:
            - request: The HTTP request object containing the data.

        Returns:
            - A response with the created or updated social URL data if successful.
            - Otherwise, returns an error response with the appropriate status code.

        Raises:
            - serializers.ValidationError: If the serializer data is invalid.

        Notes:
            This function requires the user to be a staff member. If the user is not a staff member,
            an unauthorized error response will be returned.
        """

        context = dict()
        serializer = self.get_serializer(data=request.data)
        try:
            if self.request.user.is_staff:
                serializer.is_valid(raise_exception=True)
                if SocialUrl.all_objects.filter(platform=serializer.validated_data['platform'],
                                                  is_removed=True).exists():
                    SocialUrl.all_objects.filter(platform=serializer.validated_data['platform'],
                                                 is_removed=True).update(is_removed=False)
                    social_url_instance = SocialUrl.all_objects.get(
                        platform=serializer.validated_data['platform'], is_removed=False
                    )
                    serializer.update(social_url_instance, serializer.validated_data)
                else:
                    serializer.save()
                context["data"] = serializer.data
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

    def delete(self, request, linkId):
        """
        Deletes a SocialUrl object with the specified linkId.

        Args:
            request: The HTTP request object.
            linkId (int): The ID of the SocialUrl object to be deleted.

        Returns:
            A Response object with appropriate status and data:
                - If the user is a staff member and the SocialUrl object exists, returns HTTP 200 OK
                with a success message in the data field.
                - If the user is a staff member and the SocialUrl object does not exist, returns HTTP 
                404 NOT FOUND
                with an error message in the data field.
                - If any other exception occurs, returns HTTP 404 NOT FOUND with the exception message 
                in the data field.
                - If the user is not a staff member, returns HTTP 401 UNAUTHORIZED with an error message 
                in the data field.
        """

        context = dict()
        if self.request.user.is_staff:
            try:
                SocialUrl.objects.get(id=linkId).delete()
                context['message'] = "Deleted Successfully"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except SocialUrl.DoesNotExist:
                return response.Response(
                    data={"linkId": "Does Not Exist"},
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

    def put(self, request, linkId):
        """
        Handle HTTP PUT request to update a social URL instance.

        Args:
            - request (HttpRequest): The HTTP request object.
            - linkId (int): The ID of the social URL instance to update.

        Returns:
            - Response: HTTP response indicating the result of the update.

        Raises:
            - serializers.ValidationError: If the serializer is invalid.
        """

        context = dict()
        try:
            social_url_instance = SocialUrl.all_objects.get(id=linkId)
            serializer = self.get_serializer(data=request.data, instance=social_url_instance, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                if serializer.update(social_url_instance, serializer.validated_data):
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
        except SocialUrl.DoesNotExist:
            return response.Response(
                data={"linkId": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["message"] = e
            return response.Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
            )


class AboutUsView(generics.GenericAPIView):

    permission_classes = [permissions.AllowAny]
    serializer_class = AboutUsSerializers

    def get(self, request):

        response_context = dict()
        try:
            about_us_instance = AboutUs.objects.get(title="About Our Company")
            get_data = self.serializer_class(about_us_instance)
            response_context = get_data.data
            return response.Response(
                data=response_context,
                status=status.HTTP_200_OK
            )
        except AboutUs.DoesNotExist:
            return response.Response(
                data={"description": None},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            response_context['message'] = str(e)
            return response.Response(
                data=response_context,
                status=status.HTTP_400_BAD_REQUEST
            )

    def patch(self, request):

        context = dict()
        if self.request.user.is_staff:

            if AboutUs.objects.filter(title="About Our Company").exists():
                instance = AboutUs.objects.get(title="About Our Company")
            else:
                if AboutUs.all_objects.filter(title="About Our Company", is_removed=True).exists():
                    instance = AboutUs.all_objects.get(title="About Our Company", is_removed=True)
                    instance.is_removed = False
                else:
                    instance = AboutUs.objects.create(title="About Our Company")
                instance.save()
            serializer = UpdateAboutUsSerializers(data=request.data, instance=instance, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                if serializer.update(instance, serializer.validated_data):
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


class FaqCategoryView(generics.ListAPIView):
    """
    A view for displaying a list of FAQ categories.

    Attributes:
        - permission_classes ([permissions.IsAuthenticated]): List of permission classes that the view requires. In this
            case, only authenticated users are allowed to access the view.

        - serializer_class (FaqCategorySerializers): The serializer class used for data validation and serialization.

        - queryset (QuerySet): The queryset that the view should use to retrieve the countries. By default, it is set
            to retrieve all countries using `FaqCategory.objects.all()`.

        - filter_backends ([filters.SearchFilter]): List of filter backends to use for filtering the queryset. In this
            case, only `SearchFilter` is used.

        - search_fields (list): List of fields to search for in the queryset. In this case, the field is "title".

    """

    permission_classes = [permissions.AllowAny]
    serializer_class = FaqCategorySerializers
    queryset = FaqCategory.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    pagination_class = CustomPagination

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def post(self, request):
        """
        Handle POST request to create a new FAQ category.
        The request must contain valid data for the FAQ category to be created.

        Only users with `is_staff` attribute set to True are authorized to create a FAQ category.

        Returns:
            - HTTP 201 CREATED with a message "FaqCategory added successfully" if the FAQ category is created
            successfully.
            - HTTP 400 BAD REQUEST with error message if data validation fails.
            - HTTP 401 UNAUTHORIZED with a message "You do not have permission to perform this action." if the user is
            not authorized.

        Raises:
            Exception: If an unexpected error occurs during the request handling.
        """
        context = dict()
        serializer = self.serializer_class(data=request.data)
        try:
            if self.request.user.is_staff:
                serializer.is_valid(raise_exception=True)
                if FaqCategory.all_objects.filter(title__iexact=serializer.validated_data['title'],
                                                  is_removed=True).exists():
                    FaqCategory.all_objects.filter(title__iexact=serializer.validated_data['title'],
                                                   is_removed=True).update(
                        is_removed=False)
                else:
                    serializer.save()
                context["data"] = serializer.data
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

    def delete(self, request, faqCategoryId):
        """
        Deletes an FaqCategory object with the given ID if the authenticated user is a staff and owns the
        FaqCategory.
        Args:
            request: A DRF request object.
            educationId: An integer representing the ID of the FaqCategory to be deleted.
        Returns:
            A DRF response object with a success or error message and appropriate status code.
        """
        context = dict()
        if self.request.user.is_staff:
            try:
                FaqCategory.objects.get(id=faqCategoryId).delete()
                context['message'] = "Deleted Successfully"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except FaqCategory.DoesNotExist:
                return response.Response(
                    data={"faqCategoryId": "Does Not Exist"},
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

    def put(self, request, faqCategoryId):
        """
        Update an `FaqCategory` instance with the provided data.

        Args:
            - `request (django.http.request.Request)`: The HTTP request object.
            - `faqCategoryId (int)`: The ID of the `FaqCategory` instance to update.

        Returns:
            - `django.http.response.Response`: An HTTP response object containing the updated data
            and appropriate status code.

        Raises:
            - `serializers.ValidationError`: If the provided data is invalid.
            - `FaqCategory.DoesNotExist`: If the FaqCategory instance with the given ID does not exist.
            - `Exception`: If any other error occurs during the update process.
        """

        context = dict()
        try:
            faq_category_instance = FaqCategory.all_objects.get(id=faqCategoryId)
            serializer = self.serializer_class(data=request.data, instance=faq_category_instance, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                if serializer.update(faq_category_instance, serializer.validated_data):
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
        except FaqCategory.DoesNotExist:
            return response.Response(
                data={"faqCategoryId": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["message"] = e
            return response.Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
            )


class FaqView(generics.ListAPIView):
    """
    A view for displaying a list of frequently asked questions (FAQs).

    Attributes:
        - permission_classes ([permissions.AllowAny]): List of permission classes that the view requires. In this
            case, the view allows access to any user, authenticated or not.

        - serializer_class (FAQSerializers): The serializer class used for data validation and serialization.

        - queryset (QuerySet): The queryset that the view should use to retrieve the FAQs. By default, it is set
            to retrieve all FAQs using `FAQ.objects.all()`.

        - filter_backends ([filters.SearchFilter]): List of filter backends to use for filtering the queryset. In this
            case, only `SearchFilter` is used.

        - search_fields (list): List of fields to search for in the queryset. In this case, the field is "title".

        - pagination_class (CustomPagination): The pagination class used for paginating the results.

    """

    permission_classes = [permissions.AllowAny]
    serializer_class = FAQSerializers
    queryset = FAQ.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    pagination_class = CustomPagination

    def list(self, request, role, faqCategoryId):
        """
        Retrieve a paginated list of FAQ questions based on the provided role and FAQ category ID.

        Args:
            - request (HttpRequest): The HTTP request object.
            - role (str): The role associated with the FAQ questions to retrieve.
            - faqCategoryId (int): The ID of the FAQ category to filter the questions.

        Returns:
            - Response: A paginated response containing the serialized FAQ question data.

        Raises:
            N/A

        """
    
        queryset = self.filter_queryset(self.get_queryset().filter(role=role, category_id=faqCategoryId))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def post(self, request):
        """
        Handle the HTTP POST request to create a new FAQ.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: A response object indicating the status and data.

        Raises:
            ValidationError: If the data provided in the request is not valid.

        Permissions:
            - Staff members: Allowed to create or update an FAQ.
            - Non-staff members: Unauthorized to perform the action.

        Logic:
            - If the user is a staff member:
                - Validate the serializer data.
                - If an FAQ with the same question (case-insensitive) and is_removed=True exists:
                    - Set is_removed=False for the existing FAQ.
                    - Get the updated FAQ instance.
                    - Update the serializer data with the updated FAQ instance.
                - Otherwise, save the serializer data with the current user.
                - Return a response with the serialized data and HTTP status 201 (Created).
            - If the user is not a staff member:
                - Return an unauthorized response with an appropriate message.
            - If a ValidationError occurs during data validation:
                - Return a response with the validation errors and HTTP status 400 (Bad Request).
            - If any other exception occurs:
                - Return a response with the exception message and HTTP status 400 (Bad Request).
        """

        context = dict()
        serializer = CreateFAQSerializers(data=request.data)
        try:
            if self.request.user.is_staff:
                serializer.is_valid(raise_exception=True)
                if FAQ.all_objects.filter(question__iexact=serializer.validated_data['question'],
                                                  is_removed=True).exists():
                    FAQ.all_objects.filter(question__iexact=serializer.validated_data['question'],
                                                   is_removed=True).update(
                        is_removed=False)
                    faq_instance = FAQ.all_objects.get(question__iexact=serializer.validated_data['question'],
                                                       is_removed=False)
                    serializer.update(faq_instance, serializer.validated_data)
                else:
                    serializer.save(user=request.user)
                context["data"] = serializer.data
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

    def delete(self, request, faqId):
        """
        Deletes a FAQ object with the specified ID.

        Args:
            request (HttpRequest): The HTTP request object.
            faqId (int): The ID of the FAQ object to be deleted.

        Returns:
            Response: The HTTP response indicating the result of the delete operation.

        Raises:
            FAQ.DoesNotExist: If the FAQ object with the given ID does not exist.
            Exception: If an unexpected exception occurs during the delete operation.

        """

        context = dict()
        if self.request.user.is_staff:
            try:
                FAQ.objects.get(id=faqId).delete()
                context['message'] = "Deleted Successfully"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except FAQ.DoesNotExist:
                return response.Response(
                    data={"faqId": "Does Not Exist"},
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

    def put(self, request, faqId):
        """
        Handle the HTTP PUT request to update a FAQ instance.

        Args:
            request (HttpRequest): The HTTP request object.
            faqId (int): The ID of the FAQ instance to be updated.

        Returns:
            Response: An HTTP response indicating the result of the update.

        Raises:
            serializers.ValidationError: If the provided data is invalid.
            FAQ.DoesNotExist: If the FAQ instance with the given ID does not exist.

        """

        context = dict()
        try:
            faq_instance = FAQ.all_objects.get(id=faqId)
            serializer = CreateFAQSerializers(data=request.data, instance=faq_instance, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                if serializer.update(faq_instance, serializer.validated_data):
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
        except FAQ.DoesNotExist:
            return response.Response(
                data={"faqCategoryId": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["message"] = e
            return response.Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
            )


class ResourcesDetailView(generics.GenericAPIView):

    serializer_class = ResourcesSerializers
    permission_classes = [permissions.AllowAny]

    def get(self, request, resourcesId):
        response_context = dict()
        context = dict()
        try:
            if resourcesId:
                resources_data = ResourcesContent.objects.get(id=resourcesId)
                get_data = self.serializer_class(resources_data)
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
