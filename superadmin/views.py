import io, csv, os, pathlib
from datetime import datetime, date, timedelta

from django.db.models import Q
from django_filters import rest_framework as django_filters

from rest_framework import (
    status, generics, serializers,
    response, permissions, filters
)

from core.middleware import JWTMiddleware
from core.pagination import CustomPagination

from jobs.models import (
    JobCategory, JobDetails
)
from jobs.filters import JobDetailsFilter

from users.filters import UsersFilter
from users.models import UserSession, User

from project_meta.models import (
    Country, City, EducationLevel,
    Language, Skill, Tag,
    JobSeekerCategory, Sector,
    AllCountry
)

from tenders.models import TenderCategory

from .models import Content
from .serializers import (
    CountrySerializers, CitySerializers, JobCategorySerializers,
    EducationLevelSerializers, LanguageSerializers, SkillSerializers,
    TagSerializers, ChangePasswordSerializers, ContentSerializers,
    CandidatesSerializers, JobListSerializers, UserCountSerializers,
    DashboardCountSerializers, JobSeekerCategorySerializers,
    TenderCategorySerializers, SectorSerializers
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
        queryset = self.filter_queryset(self.get_queryset())
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
        serializer = self.serializer_class(data=request.data)
        try:
            if self.request.user.is_staff:
                serializer.is_valid(raise_exception=True)
                if Country.all_objects.filter(title=serializer.validated_data['title'], is_removed=True).exists():
                    Country.all_objects.filter(title=serializer.validated_data['title'], is_removed=True).update(
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
    serializer_class = CitySerializers
    queryset = City.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    pagination_class = CustomPagination

    def list(self, request):
        country_id = request.GET.get('countryId', None)
        queryset = City.objects.all()
        if country_id:
            queryset = City.objects.filter(country_id=country_id)
        queryset = self.filter_queryset(queryset)
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
        serializer = self.serializer_class(data=request.data)
        try:
            if self.request.user.is_staff:
                serializer.is_valid(raise_exception=True)
                if City.all_objects.filter(title=serializer.validated_data['title'],
                                           country=serializer.validated_data['country'], is_removed=True).exists():
                    City.all_objects.filter(title=serializer.validated_data['title'],
                                            country=serializer.validated_data['country'], is_removed=True).update(
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
    queryset = JobCategory.objects.all()
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
                if JobCategory.all_objects.filter(title=serializer.validated_data['title'], is_removed=True).exists():
                    JobCategory.all_objects.filter(title=serializer.validated_data['title'], is_removed=True).update(
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
                if EducationLevel.all_objects.filter(title=serializer.validated_data['title'],
                                                     is_removed=True).exists():
                    EducationLevel.all_objects.filter(title=serializer.validated_data['title'], is_removed=True).update(
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
                if Language.all_objects.filter(title=serializer.validated_data['title'], is_removed=True).exists():
                    Language.all_objects.filter(title=serializer.validated_data['title'], is_removed=True).update(
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
                if Skill.all_objects.filter(title=serializer.validated_data['title'], is_removed=True).exists():
                    Skill.all_objects.filter(title=serializer.validated_data['title'], is_removed=True).update(
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
                if Tag.all_objects.filter(title=serializer.validated_data['title'], is_removed=True).exists():
                    Tag.all_objects.filter(title=serializer.validated_data['title'], is_removed=True).update(
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


class JobSeekerCategoryView(generics.ListAPIView):
    """
    A view for displaying a list of job categories.

    Attributes:
        - permission_classes ([permissions.IsAuthenticated]): List of permission classes that the view requires. In this
            case, only authenticated users are allowed to access the view.

        - serializer_class (JobSeekerCategorySerializers): The serializer class used for data validation and
            serialization.

        - queryset (QuerySet): The queryset that the view should use to retrieve the countries. By default, it is set
            to retrieve all countries using `JobSeekerCategory.objects.all()`.

        - filter_backends ([filters.SearchFilter]): List of filter backends to use for filtering the queryset. In this
            case, only `SearchFilter` is used.

        - search_fields (list): List of fields to search for in the queryset. In this case, the field is "title".

    """

    permission_classes = [permissions.AllowAny]
    serializer_class = JobSeekerCategorySerializers
    queryset = JobSeekerCategory.objects.all()
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
        Handle POST request to create a new job seeker category.
        The request must contain valid data for the job seeker category to be created.

        Only users with `is_staff` attribute set to True are authorized to create a job seeker category.

        Returns:
            - HTTP 201 CREATED with a message "JobSeekerCategory added successfully" if the job seeker category is
            created successfully.
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

    def delete(self, request, jobSeekerCategoryId):
        """
        Deletes an JobSeekerCategory object with the given ID if the authenticated user is a job seeker and owns the
        JobSeekerCategory.
        Args:
            request: A DRF request object.
            educationId: An integer representing the ID of the JobSeekerCategory to be deleted.
        Returns:
            A DRF response object with a success or error message and appropriate status code.
        """
        context = dict()
        if self.request.user.is_staff:
            try:
                JobSeekerCategory.objects.get(id=jobSeekerCategoryId).delete()
                context['message'] = "Deleted Successfully"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except JobSeekerCategory.DoesNotExist:
                return response.Response(
                    data={"jobSeekerCategoryId": "Does Not Exist"},
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
                if TenderCategory.all_objects.filter(title=serializer.validated_data['title'],
                                                     is_removed=True).exists():
                    TenderCategory.all_objects.filter(title=serializer.validated_data['title'], is_removed=True).update(
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


class SectorView(generics.ListAPIView):
    """
    A view for displaying a list of sectors .

    Attributes:
        - permission_classes ([permissions.IsAuthenticated]): List of permission classes that the view requires. In this
            case, only authenticated users are allowed to access the view.

        - serializer_class (SectorSerializers): The serializer class used for data validation and serialization.

        - queryset (QuerySet): The queryset that the view should use to retrieve the countries. By default, it is set
            to retrieve all countries using `Sector.objects.all()`.

        - filter_backends ([filters.SearchFilter]): List of filter backends to use for filtering the queryset. In this
            case, only `SearchFilter` is used.

        - search_fields (list): List of fields to search for in the queryset. In this case, the field is "title".

    """

    permission_classes = [permissions.AllowAny]
    serializer_class = SectorSerializers
    queryset = Sector.objects.all()
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
        Handle POST request to create a new sector.
        The request must contain valid data for the sector to be created.

        Only users with `is_staff` attribute set to True are authorized to create a sector.

        Returns:
            - HTTP 201 CREATED with added sector data (id, title) if the sector is created successfully.
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
                if Sector.all_objects.filter(title=serializer.validated_data['title'], is_removed=True).exists():
                    Sector.all_objects.filter(title=serializer.validated_data['title'], is_removed=True).update(
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

    def delete(self, request, sectorId):
        """
        Deletes an Sector object with the given ID if the authenticated user is a job seeker and owns the
        Sector.
        Args:
            request: A DRF request object.
            sectorId: An integer representing the ID of the Sector to be deleted.
        Returns:
            A DRF response object with a success or error message and appropriate status code.
        """
        context = dict()
        if self.request.user.is_staff:
            try:
                Sector.objects.get(id=sectorId).delete()
                context['message'] = "Deleted Successfully"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except Sector.DoesNotExist:
                return response.Response(
                    data={"sector": "Does Not Exist"},
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
                # next(io_string)
                get_data = csv.reader(io_string)
                for row in get_data:
                    if row[0].isdigit():
                        if AllCountry.objects.filter(id=row[0]).exists():
                            AllCountry.objects.filter(id=row[0]).update(
                                title=row[1], iso3=row[2], iso2=row[3],
                                numeric_code=row[4], phone_code=row[5], capital=row[6],
                                currency=row[7], currency_name=row[8], currency_symbol=row[9],
                                tld=row[10], native=row[11], region=row[12], subregion=row[13],
                                timezones=row[14], latitude=row[15], longitude=row[16],
                                emoji=row[17], emojiU=row[18]
                            )
                        else:
                            AllCountry.objects.create(
                                id=row[0], title=row[1], iso3=row[2], iso2=row[3],
                                numeric_code=row[4], phone_code=row[5], capital=row[6],
                                currency=row[7], currency_name=row[8], currency_symbol=row[9],
                                tld=row[10], native=row[11], region=row[12], subregion=row[13],
                                timezones=row[14], latitude=row[15], longitude=row[16],
                                emoji=row[17], emojiU=row[18]
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
