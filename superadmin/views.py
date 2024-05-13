import csv, io, os, pathlib
import calendar
from datetime import datetime, date, timedelta, time
import threading
from django.core.handlers.wsgi import WSGIHandler
from django.core.signals import request_finished
from django.db.models import Exists, OuterRef, Q
from django.shortcuts import get_object_or_404, HttpResponse
from django_filters import rest_framework as django_filters
from rest_framework import (
    status, generics, serializers,
    response, permissions, filters
)
from uuid import UUID
from superadmin.models import (
    Invoice, PointDetection, 
    SMTPSetting, RechargeHistory, InvoiceIcon
)

from core.middleware import JWTMiddleware
from core.pagination import CustomPagination
from core.emails import get_email_object
from core.tokens import (
    SessionTokenObtainPairSerializer
)
from employers.views import my_callback, process_description, generate_pdf_file, generate_merge_pdf_file
from jobs.filters import JobDetailsFilter
from jobs.models import (
    JobCategory, JobDetails,
    JobSubCategory
)
from jobs.serializers import GetJobsSerializers
from users.serializers import AdminSerializer
from project_meta.models import (
    Country, City, EducationLevel,
    Language, Skill, Tag,
    AllCountry, AllCity,
    Choice, OpportunityType
)
from tenders.filters import TenderDetailsFilter
from tenders.models import TenderCategory, TenderDetails
from tenders.serializers import TendersSerializers
from user_profile.models import EmployerProfile
from users.filters import UsersFilter
from users.models import UserSession, User
from users.views import create_user_session
from .filters import InvoiceDetailsFilter
from .models import (
    Content, ResourcesContent, SocialUrl,
    AboutUs, FaqCategory, FAQ, CategoryLogo,
    Testimonial, NewsletterUser, PointDetection,
    RechargeHistory, Packages, Invoice, SMTPSetting,
    GoogleAddSenseCode, Rights, UserSubRights, UserRights,
    InvoiceFooter
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
    FAQSerializers, CreateFAQSerializers, UploadLogoSerializers,
    LogoSerializers, TestimonialSerializers, GetTestimonialSerializers,
    NewsletterUserSerializers, CreateJobsSerializers, CreateTendersSerializers,
    PackageSerializers, UpdateJobSerializers, ModifyUserRightsSerializers,
    UpdateTenderSerializers, InvoiceSerializers, InvoiceDetailSerializers,
    GoogleAddSenseCodeSerializers, FinancialCountSerializers,
    UserRightsSerializers
)
from .seeds import run_seed
from .process import html_to_pdf
from koor.config.common import Common

import random, string

def generate_random_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(10))
    return password

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
            queryset = self.filter_queryset(self.get_queryset())
            # queryset = self.filter_queryset(self.get_queryset().filter(~Q(project_meta_city_country=None)))
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
                    country_instance = Country.all_objects.get(title__iexact=serializer.validated_data['title'],
                                                               is_removed=False)
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
            if 'already exists' in str(e):
                context['message'] = ['This country already exists.']
            else:
                context['message'] = [str(e)]
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
                if JobDetails.objects.filter(country__id=countryId).exists():
                    context['message'] = ["This country already used in job."]
                    return response.Response(
                        data=context,
                        status=status.HTTP_404_NOT_FOUND
                    )
                else:
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
                context["message"] = [e]
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

    
    def put(self, request, countryId):

        context = dict()
        try:
            country_instance = Country.all_objects.get(id=countryId)
            new_title = ""
            error_message = {}
            if 'title' in request.data:
                new_title = request.data['title']
            else:
                error_message['title'] = "This field is required."
            if 'currency_code' in request.data:
                new_currency_code = request.data['currency_code']
            else:
                error_message['currency_code'] = "This field is required."
            if 'country_code' in request.data:
                new_country_code = request.data['country_code']
            else:
                error_message['country_code'] = "This field is required."
            if 'iso_code2' in request.data:
                new_iso_code2 = request.data['iso_code2']
            else:
                error_message['iso_code2'] = "This field is required."
            if 'iso_code3' in request.data:
                new_iso_code3 = request.data['iso_code3']
            else:
                error_message['iso_code3'] = "This field is required."
            if error_message:
                return response.Response(
                    data=error_message,
                    status=status.HTTP_404_NOT_FOUND
                )
            if Country.all_objects.filter(title__iexact=new_title, currency_code=new_currency_code, country_code=new_country_code, iso_code2=new_iso_code2, iso_code3=new_iso_code3).exclude(id=countryId).exists():
                return response.Response(
                    data={"message": ['This country already exists.']},
                    status=status.HTTP_404_NOT_FOUND
                )
            else:
                Country.all_objects.filter(id=countryId).update(title__iexact=new_title, currency_code=new_currency_code, country_code=new_country_code, iso_code2=new_iso_code2, iso_code3=new_iso_code3)
                context['message'] = ["Updated Successfully"]
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
        except Country.DoesNotExist:
            return response.Response(
                data={"countryId": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["message"] = e
            return response.Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
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
                                           country__title=serializer.validated_data['country_name'],
                                           is_removed=True).exists():
                    City.all_objects.filter(title__iexact=serializer.validated_data['title'],
                                            country__title=serializer.validated_data['country_name'],
                                            is_removed=True).update(
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
            if 'already exists' in str(e):
                context['message'] = ['This city already exists.']
            else:
                context['message'] = [str(e)]
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
                if JobDetails.objects.filter(city__id=cityId).exists():
                    context['message'] = ["This city already used in job."]
                    return response.Response(
                        data=context,
                        status=status.HTTP_404_NOT_FOUND
                    )
                else:
                    City.objects.get(id=cityId).delete()
                    context['message'] = ["Deleted Successfully"]
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
            context['message'] = ["You do not have permission to perform this action."]
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
            )

    def put(self, request, cityId):

        context = dict()
        try:
            city_instance = City.all_objects.get(id=cityId)
            new_title = ""
            new_country_name = ""
            if 'title' in request.data:
                new_title = request.data['title']
            else:
                return response.Response(
                    data={"title": "This field is required."},
                    status=status.HTTP_404_NOT_FOUND
                )
            if 'country_name' in request.data:
                new_country_name = request.data['country_name']
            else:
                return response.Response(
                    data={"country_name": "This field is required."},
                    status=status.HTTP_404_NOT_FOUND
                )
            if City.all_objects.filter(title__iexact=new_title, country__title=new_country_name).exclude(id=cityId).exists():
                return response.Response(
                    data={"message": ['This city already exists.']},
                    status=status.HTTP_404_NOT_FOUND
                )
            else:
                City.all_objects.filter(id=cityId).update(title=new_title, country=new_country_name)
                context['message'] = ["Updated Successfully"]
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
        except City.DoesNotExist:
            return response.Response(
                data={"cityId": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["message"] = e
            return response.Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
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
                context['message'] = ["You do not have permission to perform this action."]
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
            context['message'] = [str(e)]
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
                if JobDetails.objects.filter(job_category__id=jobCategoryId).exists():
                    context['message'] = ["This category already used in job."]
                    return response.Response(
                        data=context,
                        status=status.HTTP_404_NOT_FOUND
                    )
                else:
                    JobCategory.objects.get(id=jobCategoryId).delete()
                    context['message'] = ["Deleted Successfully"]
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
            context['message'] = ["You do not have permission to perform this action."]
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
                    context['message'] = ["Updated Successfully"]
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
                if JobDetails.objects.filter(highest_education__id=educationLevelId).exists():
                    context['message'] = ["This education already used in job."]
                    return response.Response(
                        data=context,
                        status=status.HTTP_404_NOT_FOUND
                    )
                else:
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
                context['message'] = ["You do not have permission to perform this action."]
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
            context['message'] = [str(e)]
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
                context['message'] = ["Deleted Successfully"]
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
                context["message"] = [e]
                return response.Response(
                    data=context,
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            context['message'] = ["You do not have permission to perform this action."]
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
                    context['message'] = ["Updated Successfully"]
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
    queryset = Skill.objects.all().order_by('title')
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
                if JobDetails.objects.filter(skill__id=skillId).exists():
                    context['message'] = ["This skill already used in job."]
                    return response.Response(
                        data=context,
                        status=status.HTTP_404_NOT_FOUND
                    )
                else:
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
                
                user_session = create_user_session(request, serializer.validated_data)
                token = SessionTokenObtainPairSerializer.get_token(
                    user=serializer.validated_data,
                    session_id=user_session.id
                )

                response_context["message"] = "Password update successfully."
                return response.Response(
                    data=response_context,
                    headers={"x-access": token.access_token, "x-refresh": token},
                    status=status.HTTP_201_CREATED
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
    queryset = User.objects.all().order_by('-date_joined')
    filter_backends = [filters.SearchFilter, django_filters.DjangoFilterBackend]
    filterset_class = UsersFilter
    search_fields = ['name', 'email']
    pagination_class = CustomPagination

    def list(self, request):
        context = dict()
        if self.request.user.is_staff:
            start_date = self.request.GET.get('from', None)
            end_date = self.request.GET.get('to', None)
            if end_date:
                end_date = datetime.strptime(str(end_date), '%Y-%m-%d')
                end_date = datetime.combine(end_date.date(), time(hour=23, minute=59, second=59))
            if start_date:
                queryset = self.filter_queryset(self.get_queryset().filter(
                    Q(role="job_seeker") | Q(role="vendor")
                ).filter(
                    date_joined__gte=start_date,
                    date_joined__lte=end_date,
                ))
            else:
                queryset = self.filter_queryset(self.get_queryset().filter(Q(role="job_seeker") | Q(role="vendor")))
            action = request.GET.get('action', None)
            if action == 'download':
                directory_path = create_directory()
                file_name = '{0}/{1}'.format(directory_path, 'candidate.csv')
                with open(file_name, mode='w') as data_file:
                    file_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    file_writer.writerow(
                        ["Number", "Role", "Name", "Email", "Mobile Number", "Registration Date"]
                    )
                    for counter, rows in enumerate(queryset):
                        mobile_number = "None"
                        if rows.country_code:
                            mobile_number = str(rows.country_code) + str(rows.mobile_number)
                        file_writer.writerow(
                            [
                                str(counter + 1), str(rows.role), str(rows.name),
                                str(rows.email), mobile_number, str(rows.date_joined.date())
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
    queryset = User.objects.all().order_by('-date_joined')
    filter_backends = [filters.SearchFilter, django_filters.DjangoFilterBackend]
    filterset_class = UsersFilter
    search_fields = ['name', 'email']
    pagination_class = CustomPagination

    def list(self, request):
        context = dict()
        if self.request.user.is_staff:
            start_date = self.request.GET.get('from', None)
            end_date = self.request.GET.get('to', None)
            if end_date:
                end_date = datetime.strptime(str(end_date), '%Y-%m-%d')
                end_date = datetime.combine(end_date.date(), time(hour=23, minute=59, second=59))
            if start_date:
                queryset = self.filter_queryset(self.get_queryset().filter(
                    role="employer",
                    date_joined__gte=start_date,
                    date_joined__lte=end_date,
                ))
            else:
                queryset = self.filter_queryset(self.get_queryset().filter(role="employer"))
            action = request.GET.get('action', None)
            if action == 'download':
                directory_path = create_directory()
                file_name = '{0}/{1}'.format(directory_path, 'employers.csv')
                with open(file_name, mode='w') as data_file:
                    file_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    file_writer.writerow(
                        ["Number", "Name", "Email", "Mobile Number", "Registration Date"]
                    )
                    for counter, rows in enumerate(queryset):
                        mobile_number = "None"
                        if rows.country_code:
                            mobile_number = str(rows.country_code) + str(rows.mobile_number)
                        file_writer.writerow(
                            [
                                str(counter + 1), str(rows.name), str(rows.email),
                                mobile_number, str(rows.date_joined.date())
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
        try:
            employer_instance = EmployerProfile.objects.get(user_id=employerId)
        except EmployerProfile.DoesNotExist:
            return response.Response(data={"employerId": "Does Not Exist"}, status=status.HTTP_404_NOT_FOUND)

        response_context = {'message': ''}
        context = dict()
        if action == 'verify':
            if not self.request.user.is_staff:
                response_context = {'message': "You do not have permission to perform this action."}
                return response.Response(data=response_context, status=status.HTTP_401_UNAUTHORIZED)
            if employer_instance.is_verified:
                response_context['message'] = "Employer is already verified"
            else:
                employer_instance.is_verified = True
                employer_instance.save()
                context["user_name"] = employer_instance.user.name
                context["user_email"] = str(employer_instance.user.email)
                get_email_object(
                    subject=f'Account Verification Completed: Welcome to KOOR!',
                    email_template_name='email-templates/new/admin-verify-employer-account.html',
                    context=context,
                    to_email=[employer_instance.user.email, ]
                )
                response_context['message'] = "Employer verified."
        elif action == 'unverify':
            if not self.request.user.is_staff:
                response_context = {'message': "You do not have permission to perform this action."}
                return response.Response(data=response_context, status=status.HTTP_401_UNAUTHORIZED)
            if not employer_instance.is_verified:
                response_context['message'] = "Employer is not verified"
            else:
                employer_instance.is_verified = False
                employer_instance.save()
                response_context['message'] = "Employer unverified."
        elif action == 'recharge':
            employer_instance.points = employer_instance.points + int(request.data.get('points', 0))
            employer_instance.save()
            email_context=dict()
            email_context["yourname"] = employer_instance.user.name
            email_context["recharge_point"] = int(request.data.get('points', 0))
            email_context["current_point"] = employer_instance.points
            email_context["recharge_amount"] = int(request.data.get('amount', 0))
            if employer_instance.user.email:
                get_email_object(
                    subject=f'Your account recharge by Koor Jobs',
                    email_template_name='email-templates/recharge-points.html',
                    context=email_context,
                    to_email=[employer_instance.user.email, ]
                )
            RechargeHistory.objects.create(
                user=employer_instance.user, 
                points=int(request.data.get('points', 0)),
                amount=int(request.data.get('amount', 0)),
                note=request.data.get('note', ''),
                package=request.data.get('package', 'none')
                )
            response_context['message'] = "Point credited."
        else:
            response_context['message'] = "Invalid action"

        return response.Response(data=response_context, status=status.HTTP_200_OK)


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
            start_date = self.request.GET.get('from', None)
            end_date = self.request.GET.get('to', None)
            if end_date:
                end_date = datetime.strptime(str(end_date), '%Y-%m-%d')
                end_date = datetime.combine(end_date.date(), time(hour=23, minute=59, second=59))
            if start_date:
                filter_type = self.request.GET.get('filterType', None)
                if filter_type == 'closed':
                    queryset = queryset.filter(deadline__lt=date.today())
                else:
                    queryset = queryset.filter(deadline__gte=date.today())
                queryset = queryset.filter(
                    created__gte=start_date,
                    created__lte=end_date,
                )
            if action == 'download':
                directory_path = create_directory()
                file_name = '{0}/{1}'.format(directory_path, 'jobs.csv')
                with open(file_name, mode='w') as data_file:
                    file_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    file_writer.writerow(
                        ["Number", "Job ID", "Job Title", "Company", "Location", "Created At"])
                    for counter, rows in enumerate(queryset):
                        location = "None"
                        if rows.city:
                            location = str(rows.city) + ", " + str(rows.country)
                        if rows.user:
                            user_name = str(rows.user.name)
                        elif rows.company:
                            user_name = str(rows.company)
                        else:
                            user_name = ""
                        file_writer.writerow(
                            [
                                str(counter + 1), str(rows.job_id), str(rows.title),
                                str(user_name), location, str(rows.created.date())
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
        response_context = dict()
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
                end_date = datetime.strptime(str(end_date), '%Y-%m-%d')
                end_date = datetime.combine(end_date.date(), time(hour=23, minute=59, second=59))
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
                serializer = self.get_serializer(queryset, context=context)
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
                end_date = datetime.strptime(str(end_date), '%Y-%m-%d')
                end_date = datetime.combine(end_date.date(), time(hour=23, minute=59, second=59))
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

class CoreUpdateView(generics.GenericAPIView):
    
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        response_context = dict()
        user_context = dict()
        try:
            employer = User.objects.filter(role='employer', user_profile_employerprofile_user__is_verified=True).count()
            jobs = JobDetails.objects.filter(status='active', created__date=date.today()).count()
            tenders = TenderDetails.objects.filter(status='active', deadline__gte=date.today()).count()
            employer = User.objects.filter(role='employer', user_profile_employerprofile_user__is_verified=True).count()
            return response.Response(
                data={'jobs':jobs, 'employer':employer, 'tenders':tenders},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            response_context['message'] = str(e)
            return response.Response(
                data=response_context,
                status=status.HTTP_400_BAD_REQUEST
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
                if JobDetails.objects.filter(job_sub_category__id=jobSubCategoryId).exists():
                    context['message'] = ["This subcategory already used in job."]
                    return response.Response(
                        data=context,
                        status=status.HTTP_404_NOT_FOUND
                    )
                else:
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
                if Choice.all_objects.filter(title__iexact=serializer.validated_data['title'],
                                             is_removed=True).exists():
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
                if OpportunityType.all_objects.filter(title__iexact=serializer.validated_data['title'],
                                                      is_removed=True).exists():
                    OpportunityType.all_objects.filter(title__iexact=serializer.validated_data['title'],
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
            start_date = self.request.GET.get('from', None)
            end_date = self.request.GET.get('to', None)
            if end_date:
                end_date = datetime.strptime(str(end_date), '%Y-%m-%d')
                end_date = datetime.combine(end_date.date(), time(hour=23, minute=59, second=59))
            if start_date:
                filter_type = self.request.GET.get('filterType', None)
                if filter_type == 'closed':
                    queryset = queryset.filter(deadline__lt=date.today())
                else:
                    queryset = queryset.filter(deadline__gte=date.today())
                queryset = queryset.filter(
                    created__gte=start_date,
                    created__lte=end_date,
                )
            if action == 'download':
                directory_path = create_directory()
                file_name = '{0}/{1}'.format(directory_path, 'tenders.csv')
                with open(file_name, mode='w') as data_file:
                    file_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    file_writer.writerow(
                        ["Number", "Tender ID", "Tender Title", "Company",
                         "Tag", "Tender Category", "Tender Type", "Sector",
                         "Location", "Created At"])
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
                        if rows.user:
                            user_name = str(rows.user.name)
                        elif rows.company:
                            user_name = str(rows.company)
                        else:
                            user_name = ""
                        file_writer.writerow(
                            [
                                str(counter + 1), str(rows.tender_id), str(rows.title),
                                str(user_name), tag, tender_category, tender_type,
                                sector, location, str(rows.created.date())
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
    search_fields = ['title', 'role']
    pagination_class = CustomPagination

    def list(self, request):
        role = request.GET.get('role', None)
        if role:
            queryset = self.filter_queryset(self.get_queryset().filter(role=role))
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
                                                  role__iexact=serializer.validated_data['role'],
                                                  is_removed=True).exists():
                    FaqCategory.all_objects.filter(title__iexact=serializer.validated_data['title'],
                                                   role__iexact=serializer.validated_data['role'],
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
    search_fields = ['category__title', 'answer', 'question']
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
                    if 'question' in serializer.validated_data:
                        if FAQ.objects.filter(question__iexact=serializer.validated_data['question'],
                                              is_removed=False).exists():
                            context['question'] = [serializer.validated_data['question'] + ' already exist.']
                            return response.Response(
                                data=context,
                                status=status.HTTP_400_BAD_REQUEST
                            )
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
                if 'question' in serializer.validated_data:
                    if FAQ.objects.filter(question__iexact=serializer.validated_data['question'],
                                          is_removed=False).exclude(id=faqId).exists():
                        context['question'] = [serializer.validated_data['question'] + ' already exist.']
                        return response.Response(
                            data=context,
                            status=status.HTTP_400_BAD_REQUEST
                        )
                if serializer.update(faq_instance, serializer.validated_data):
                    context['message'] = "Updated Successfully."
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


class ResourcesMoreView(generics.ListAPIView):
    serializer_class = ResourcesSerializers
    permission_classes = [permissions.AllowAny]
    queryset = ResourcesContent.objects.all().order_by('-created')
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    pagination_class = CustomPagination

    def list(self, request, resourcesId):
        context = dict()
        queryset = self.filter_queryset(self.get_queryset().exclude(id=resourcesId))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)
        


class UploadLogo(generics.ListAPIView):
    """
    A view for uploading logos.

    This class-based view handles the HTTP POST request for uploading logos.
        - It uses the specified serializer to validate the request data and save the logo.
        - If the data is valid, the view returns the URL of the saved logo with a status code of 201.
        - If there are validation errors, the view returns the error details with a status code of 400.

    Attributes:
        - serializer_class (Serializer): The serializer class used to validate and save the logo.
        - permission_classes (list): A list of permission classes applied to the view.

    Methods:
        - post(request): Handles the POST request for uploading logos.

    Raises:
        - serializers.ValidationError: If the provided data is invalid according to the serializer.

    Returns:
        - A Response object containing the result of the upload operation.

    """

    permission_classes = [permissions.AllowAny]
    serializer_class = LogoSerializers
    queryset = CategoryLogo.objects.filter(status=True)

    def list(self, request):
        """
        Retrieves a list of serialized data.

        This method retrieves a list of data by executing the queryset specified in the class.
        It filters the queryset based on the request parameters and applies any necessary serialization.
        The resulting serialized data is returned in the response.

        Parameters:
            request (Request): The request object containing information about the client's request.

        Returns:
            A Response object containing the serialized data as the response payload.

        Example Usage:
            # Create an instance of the class containing the `list` method
            instance = ClassName()

            # Create a request object
            request = Request()

            # Invoke the `list` method
            response = instance.list(request)
        """

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def post(self, request):
        """
        Handles the HTTP POST request for uploading logos.

        Parameters:
            request (HttpRequest): The request object containing the logo data.

        Returns:
            A Response object containing the result of the upload operation.
        """

        serializer = UploadLogoSerializers(data=request.data)
        try:
            if self.request.user.is_staff:
                serializer.is_valid(raise_exception=True)
                get_url = serializer.save()
                return response.Response(data=get_url, status=status.HTTP_201_CREATED)
            else:
                return response.Response(
                    data={'message': "You do not have permission to perform this action."},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except serializers.ValidationError:
            return response.Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, logoId):
        """
        Deletes a category logo.

        - This method handles the HTTP DELETE request to delete a category logo with the specified logoId.
        - If the user making the request is a staff member, the category logo is deleted from the database.
        - If the logo is found and deleted successfully, a success message is returned with a status code 
            of 200.
        - If the logo does not exist, a corresponding error message is returned with a status code of 404.
        - If any other exception occurs during the deletion process, the exception message is returned with 
            a status code of 404.
        - If the user is not a staff member, an unauthorized message is returned with a status code of 401.

        Parameters:
            - request (HttpRequest): The request object containing the user making the request.
            - logoId (int): The ID of the category logo to be deleted.

        Returns:
            - A Response object containing the result of the deletion operation.

        Example Usage:
            # Create an instance of the view
            view = CategoryLogo()

            # Make a DELETE request to delete a category logo with ID 42
            request = HttpRequest()
            response = view.delete(request, 42)
        """

        context = dict()
        if self.request.user.is_staff:
            try:
                CategoryLogo.objects.get(id=logoId).delete()
                context['message'] = "Deleted Successfully"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except CategoryLogo.DoesNotExist:
                return response.Response(
                    data={"logoId": "Does Not Exist"},
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


class TestimonialView(generics.ListAPIView):
    """
    A view for retrieving a list of testimonials.

    This view allows both staff and non-staff users to retrieve a list of testimonials.
    The testimonials can be filtered by title using the search functionality.
    Pagination is applied to the results.

    Attributes:
        - permission_classes (list): A list of permission classes for the view. AllowAny is used, meaning all users
            have access.
        - serializer_class: The serializer class used for serializing and deserializing testimonial data.
        - queryset: The queryset representing the testimonials to be retrieved.
        - filter_backends (list): A list of filter backends for the view. SearchFilter is used for title filtering.
        - search_fields (list): A list of fields that can be searched for filtering the testimonials.
        - pagination_class: The pagination class used for paginating the testimonials.

    """

    permission_classes = [permissions.AllowAny]
    serializer_class = GetTestimonialSerializers
    queryset = Testimonial.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    pagination_class = CustomPagination

    def list(self, request):
        """
        Retrieves a paginated list of testimonials.

        Args:
            request: The HTTP request object.

        Returns:
            A paginated response containing serialized testimonial data.

        """

        queryset = self.filter_queryset(self.get_queryset()) if self.request.user.is_staff else self.filter_queryset(
            self.get_queryset().filter(status=True))
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True) if page is not None else self.get_serializer(
            queryset, many=True)
        return self.get_paginated_response(serializer.data) if page is not None else response.Response(serializer.data)

    def post(self, request):
        """
        Create a new testimonial.

        Args:
            request: The HTTP request object.

        Returns:
            A Response object with the created testimonial data and status code 201 if successful, or a Response object
             with an error message and status code 400 if there are validation errors or any other exception occurs
             during the process.

        Raises:
            serializers.ValidationError: If the serializer validation fails.

        """

        context = dict()
        serializer = TestimonialSerializers(data=request.data)
        if not self.request.user.is_staff:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(data=context, status=status.HTTP_401_UNAUTHORIZED)

        try:
            serializer.is_valid(raise_exception=True)
            self.update_testimonial(serializer.validated_data['title'])
            serializer.save()
            context['data'] = serializer.data
            context['data']['image'] = self.get_testimonial_image(serializer.data['id'])
            return response.Response(data=context, status=status.HTTP_201_CREATED)
        except (serializers.ValidationError, Exception) as e:
            context['message'] = str(e)
            return response.Response(data=context, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, testimonialId):
        """
        Delete a testimonial.

        Args:
            request: The HTTP request object.
            testimonialId (int): The ID of the testimonial to delete.

        Returns:
            A response containing the result of the deletion operation.

        Raises:
            Testimonial.DoesNotExist: If the testimonial with the specified ID does not exist.
            Exception: If an error occurs during the deletion process.

        """

        context = dict()
        if not self.request.user.is_staff:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(data=context, status=status.HTTP_401_UNAUTHORIZED)

        try:
            testimonial = Testimonial.objects.get(id=testimonialId)
            testimonial.delete()
            context['message'] = "Deleted Successfully"
            return response.Response(data=context, status=status.HTTP_200_OK)
        except Testimonial.DoesNotExist:
            return response.Response(data={"testimonialId": "Does Not Exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            context['message'] = str(e)
            return response.Response(data=context, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, testimonialId):
        """
        Update a testimonial.

        Args:
            - request (HttpRequest): The HTTP request object.
            - testimonialId (int): The ID of the testimonial to be updated.

        Returns:
            - HttpResponse: The HTTP response containing the result of the update operation.

        Raises:
            - Testimonial.DoesNotExist: If the testimonial with the given ID does not exist.
            - serializers.ValidationError: If the serializer encounters a validation error.
            - Exception: If an unexpected exception occurs during the update process.
        """

        context = dict()
        try:
            testimonial_instance = Testimonial.all_objects.get(id=testimonialId)
            serializer = TestimonialSerializers(data=request.data, instance=testimonial_instance, partial=True)
            serializer.is_valid(raise_exception=True)
            if serializer.update(testimonial_instance, serializer.validated_data):
                context['message'] = "Updated Successfully"
                return response.Response(data=context, status=status.HTTP_200_OK)
        except Testimonial.DoesNotExist:
            return response.Response(data={"testimonialId": "Does Not Exist"}, status=status.HTTP_404_NOT_FOUND)
        except (serializers.ValidationError, Exception) as e:
            context['message'] = str(e)
            return response.Response(data=context, status=status.HTTP_404_NOT_FOUND)

    def get_filtered_queryset(self):
        """
        Retrieve the filtered queryset based on the user's staff status.

        If the user is a staff member, the function returns the filtered queryset obtained by calling
        `filter_queryset` on the original queryset.

        If the user is not a staff member, the function returns the filtered queryset obtained by calling
        `filter_queryset` on the original queryset and further filtering it based on the `status` field being `True`.

        Returns:
            QuerySet: The filtered queryset based on the user's staff status.

        """

        if self.request.user.is_staff:
            return self.filter_queryset(self.get_queryset())
        else:
            return self.filter_queryset(self.get_queryset().filter(status=True))

    def update_testimonial(self, title):
        """
        Updates the status of a testimonial by setting 'is_removed' to False if a testimonial with the given title
        exists and its 'is_removed' field is currently set to True.

        Args:
            title (str): The title of the testimonial to update.

        Returns:
            None
        """

        testimonial_qs = Testimonial.all_objects.filter(title__iexact=title, is_removed=True)
        if testimonial_qs.exists():
            testimonial_qs.update(is_removed=False)

    def get_testimonial_image(self, testimonial_id):
        """
        Retrieves the image file path URL associated with a testimonial.

        Args:
            testimonial_id (int): The ID of the testimonial.

        Returns:
            str or None: The file path URL of the testimonial image if it exists,
                         otherwise None.

        Raises:
            Testimonial.DoesNotExist: If the testimonial with the given ID does not exist.
        """

        testimonial_instance = Testimonial.objects.get(id=testimonial_id)
        return testimonial_instance.image.file_path.url if testimonial_instance.image else None


class TestimonialDetailView(generics.GenericAPIView):
    serializer_class = GetTestimonialSerializers
    permission_classes = [permissions.AllowAny]

    def get(self, request, testimonialId):
        response_context = dict()
        context = dict()
        try:
            testimonial_data = Testimonial.objects.get(id=testimonialId)
            get_data = self.serializer_class(testimonial_data)
            response_context = get_data.data
            return response.Response(
                data=response_context,
                status=status.HTTP_200_OK
            )
        except Testimonial.DoesNotExist:
            return response.Response(
                data={"testimonialId": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            response_context["message"] = str(e)
            return response.Response(
                data=response_context,
                status=status.HTTP_400_BAD_REQUEST
            )


class NewsletterUserView(generics.ListAPIView):
    """
    API view for retrieving a list of newsletter users.

    This view allows retrieval of a paginated list of newsletter users.
    The list can be filtered by searching for email addresses.

    Permissions:
    - This view allows access to any user (permission class: AllowAny).

    Serializer:
    - NewsletterUserSerializers: Serializer class for serializing the newsletter user data.

    Queryset:
    - NewsletterUser.objects.all(): Retrieves all newsletter users.

    Filters:
    - SearchFilter: Allows filtering of newsletter users based on email address.

    Pagination:
    - CustomPagination: Custom pagination class for paginating the results.

    HTTP Methods:
    - GET: Retrieve a paginated list of newsletter users.

    Usage:
    - Send a GET request to retrieve a paginated list of newsletter users.
    - Use the search parameter to filter the list based on email addresses.

    Example:
    - GET /newsletter/users/?search=test@example.com
      Retrieves a paginated list of newsletter users with email addresses matching 'test@example.com'.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = NewsletterUserSerializers
    queryset = NewsletterUser.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['email']
    pagination_class = CustomPagination

    def list(self, request):
        """
        Retrieve a paginated list of testimonials.

        Args:
            request: The request object containing the incoming request data.

        Returns:
            A response containing the paginated list of testimonials serialized as data.

        """

        queryset = self.filter_queryset(self.get_queryset())
        action = request.GET.get('action', None)
        if action == 'download':
            directory_path = create_directory()
            file_name = '{0}/{1}'.format(directory_path, 'newsletterusers.csv')
            with open(file_name, mode='w') as data_file:
                file_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                file_writer.writerow(
                    ["Number", "Role", "Email"]
                )
                for counter, rows in enumerate(NewsletterUser.objects.all()):
                    file_writer.writerow(
                        [
                            str(counter + 1), str(rows.role), str(rows.email)
                        ]
                    )
            return response.Response(
                data={"url": "/" + file_name},
                status=status.HTTP_200_OK
            )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def post(self, request):
        """
        Handles the HTTP POST request to create a new testimonial.

        Args:
            request: The HTTP request object.

        Returns:
            A response containing the created testimonial data if the request is successful and the user has permission.
            If the user doesn't have permission, returns an unauthorized response.
            If the request data is invalid, returns a response with the validation errors.
            If any other exception occurs, returns a response with the error message.

        Raises:
            N/A
        """

        context = dict()
        serializer = self.serializer_class(data=request.data)
        try:
            role = 'user'
            if self.request.user.is_authenticated :
                if self.request.user.role != 'admin':
                    role = self.request.user.role
            serializer.is_valid(raise_exception=True)
            serializer.save(role=role)
            context["data"] = serializer.data
            return response.Response(
                data=context,
                status=status.HTTP_201_CREATED
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

    def delete(self, request, newsletterId):
        """
        Delete a newsletter user.

        Args:
            request: The HTTP request.
            newsletterId (int): The ID of the newsletter user to be deleted.

        Returns:
            A response containing the result of the deletion operation.

        Raises:
            NewsletterUser.DoesNotExist: If the newsletter user with the given ID does not exist.
            Exception: If an unexpected exception occurs during the deletion process.
        """

        context = dict()
        if self.request.user.is_staff:
            try:
                NewsletterUser.objects.get(id=newsletterId).delete()
                context['message'] = "Deleted Successfully"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except NewsletterUser.DoesNotExist:
                return response.Response(
                    data={"newsletterId": "Does Not Exist"},
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


class SetPointsView(generics.GenericAPIView):
    """
    API view for retrieving and updating point data.

    This view requires authentication for all requests.

    Attributes:
        permission_classes (list): A list of permission classes for authentication.

    Methods:
        get(self, request): Retrieves the point data from the database.
        patch(self, request): Updates the point data in the database.

    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Retrieve the first point from the PointDetection objects and return it in the response.

        Args:
            request (rest_framework.request.Request): The incoming request object.

        Returns:
            rest_framework.response.Response: A response object containing the point value or None.

        Raises:
            None.
        """

        point_data = PointDetection.objects.values('points').first()
        point = point_data['points'] if point_data else None
        return response.Response(
            data={'point': point},
            status=status.HTTP_200_OK
        )

    def patch(self, request):
        """
        Updates the 'points' field of the PointDetection object.

        Args:
            request: The HTTP request object containing the updated 'point' value in the request data.

        Returns:
            A response indicating the result of the update operation. If the user is a staff member and 
            the update operation is successful, a response with status code 200 and the updated 'point' 
            value is returned. Otherwise, a response with status code 401 and an appropriate error 
            message is returned.
        """

        context = {}
        point = request.data.get('point')
        if self.request.user.is_staff:
            point_data = PointDetection.objects.first()
            if point_data:
                point_data.points = point
                point_data.save(update_fields=['points'])
            else:
                PointDetection.objects.create(points=point)
            context['point'] = point
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


class JobsCreateView(generics.ListAPIView):
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
        try:
            user_instance = None
            send_invoice_automatically= None
            if 'send_invoice_automatically' in request.data:
                send_invoice_automatically = request.data['send_invoice_automatically']
            send_email_automatically= None
            if 'send_email_automatically' in request.data:
                send_email_automatically = request.data['send_email_automatically']
            if 'employer_id' in request.data:
                employerId = request.data['employer_id']
                serializer = CreateJobsSerializers(data=request.data)
                user_instance = User.objects.get(id=employerId)
                employer_profile_instance = get_object_or_404(EmployerProfile, user=user_instance)
                point_data = PointDetection.objects.first()
                if user_instance.role == "employer":
                    serializer.is_valid(raise_exception=True)
                    if employer_profile_instance.points < point_data.points:
                        context["message"] = "This company have not enough points to create a new job."
                        return response.Response(data=context, status=status.HTTP_400_BAD_REQUEST)

                    job_instance = serializer.save(user_instance)
                    remaining_points = employer_profile_instance.points - point_data.points
                    employer_profile_instance.points = remaining_points
                    employer_profile_instance.save()
                    
                    total = float(point_data.points)
                    discount = float(point_data.points)
                    grand_total = float(point_data.points) - discount
                
                    invoice_instance = Invoice.objects.create(
                        user=user_instance, job=job_instance, points=point_data.points,
                        total=total, discount=discount, grand_total=grand_total
                    )
                    if send_email_automatically == 'False':
                        email_context["yourname"] = employer_profile_instance.user.name
                        email_context["type"] = 'job'
                        email_context['Ctype'] = 'Job'
                        email_context["title"] = request.data['title']
                        email_context["job_id"] = job_instance.job_id
                        email_context["job_link"] = Common.FRONTEND_BASE_URL + "/jobs/details/" + str(job_instance.slug)
                        email_context["discription"] = process_description(job_instance.description)
                        
                        if employer_profile_instance.user.email:
                            get_email_object(
                                subject=f'Koor Published: ' + str(request.data['title']),
                                email_template_name='email-templates/create-jobs.html',
                                context=email_context,
                                to_email=[employer_profile_instance.user.email, ]
                            )
                    if send_invoice_automatically == 'True':
                            # invoice_month = calendar.month_name[datetime.now().month]
                            if invoice_instance.start_date:
                                invoice_month = calendar.month_name[invoice_instance.start_date.month]
                            else:
                                invoice_month = calendar.month_name[invoice_instance.created.month]
                            email_context["invoice_month"] = invoice_month
                            # Send the email
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
                    # request_finished.connect(my_callback, sender=WSGIHandler, dispatch_uid='notification_trigger_callback')
                    return response.Response(data=context, status=status.HTTP_201_CREATED)
                else:
                    context['message'] = "This company have not permission to create a new job."
                    return response.Response(data=context, status=status.HTTP_401_UNAUTHORIZED)
            else:
                serializer = CreateJobsSerializers(data=request.data)
                serializer.is_valid(raise_exception=True)
                if 'company_email' in request.data:
                    if User.objects.filter(email=request.data['company_email']).exists():
                        user_instance = User.objects.get(email=request.data['company_email'])
                    else:
                        user_instance = User.objects.create(
                            role="employer", is_company=True, is_verified=True, is_active=True, 
                            email=request.data['company_email'], name=request.data['company']
                        )
                        password = generate_random_password()
                        user_instance.set_password(password)
                        user_instance.save()
                        description = ""
                        if 'company_about' in request.data:
                            description=request.data['company_about']
                        EmployerProfile.objects.create(
                            user=user_instance, description=description, is_verified=True
                        )
                        email_context["yourname"] = user_instance.name
                        email_context["type"] = 'job'
                        email_context["title"] = request.data['title']
                        email_context["password"] = password
                        email_context["youremail"] = request.data['company_email']
                        if user_instance.email:
                            if send_email_automatically == 'False':
                                get_email_object(
                                    subject=f'Koor jobs create account for you',
                                    email_template_name='email-templates/create-account.html',
                                    context=email_context,
                                    to_email=[user_instance.email, ]
                                )
                if EmployerProfile.objects.filter(user=user_instance).exists():
                    employer_profile_instance = get_object_or_404(EmployerProfile, user=user_instance)
                else:
                    description = ""
                    if 'company_about' in request.data:
                        description=request.data['company_about']
                    employer_profile_instance = EmployerProfile(
                                        user=user_instance, description=description, is_verified=True
                    )
                    employer_profile_instance.save()
                point_data = PointDetection.objects.first()
                if user_instance.role == "employer":
                    serializer.is_valid(raise_exception=True)
                    if employer_profile_instance.points < point_data.points:
                        context["message"] = "This company have not enough points to create a new job."
                        return response.Response(data=context, status=status.HTTP_400_BAD_REQUEST)
                                    
                job_instance = serializer.save(user_instance)
                remaining_points = employer_profile_instance.points - point_data.points
                employer_profile_instance.points = remaining_points
                employer_profile_instance.save()
                
                total = float(point_data.points)
                discount = float(point_data.points)
                grand_total = float(point_data.points) - discount
            
                invoice_instance = Invoice.objects.create(
                    user=user_instance, job=job_instance, points=point_data.points,
                    total=total, discount=discount, grand_total=grand_total
                )
                if send_email_automatically == 'False':
                    email_context["yourname"] = user_instance.name
                    email_context["type"] = 'job'
                    email_context["youremail"] = request.data['company_email']
                    email_context['Ctype'] = 'Job'
                    email_context["title"] = request.data['title']
                    email_context["job_id"] = job_instance.job_id
                    email_context["job_link"] = Common.FRONTEND_BASE_URL + "/jobs/details/" + str(job_instance.slug)
                    email_context["discription"] = process_description(job_instance.description)
                    if user_instance.email:
                        get_email_object(
                            subject=f'Koor Published: ' + str(request.data['title']),
                            email_template_name='email-templates/create-jobs.html',
                            context=email_context,
                            to_email=[user_instance.email, ]
                        )

                if send_invoice_automatically == 'True':
                    # invoice_month = calendar.month_name[datetime.now().month]
                    if invoice_instance.start_date:
                        invoice_month = calendar.month_name[invoice_instance.start_date.month]
                    else:
                        invoice_month = calendar.month_name[invoice_instance.created.month]
                    email_context["invoice_month"] = invoice_month
                    # email_context["invoice_month"] = invoice_month
                    # Send the email
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
                return response.Response(data=context, status=status.HTTP_201_CREATED)
            return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return response.Response(
                data={"employerId": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["message"] = str(e)
            return response.Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
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
        email_context = dict()
        try:
            job_instance = JobDetails.objects.get(id=jobId)
            serializer = UpdateJobSerializers(data=request.data, instance=job_instance, partial=True)
            send_email_automatically= None
            if 'send_email_automatically' in request.data:
                send_email_automatically = request.data['send_email_automatically']
            if 'employer_id' in request.data:
                employerId = request.data['employer_id']
                user_instance = User.objects.get(id=employerId)
                JobDetails.objects.filter(id=jobId).update(user=user_instance)
            else:
                if 'company_email' in request.data:
                    if User.objects.filter(email=request.data['company_email']).exists():
                        user_instance = User.objects.get(email=request.data['company_email'])
                    else:
                        user_instance = User.objects.create(
                            role="employer", is_company=True, is_verified=True, is_active=True, 
                            email=request.data['company_email'], name=request.data['company']
                        )
                        password = generate_random_password()
                        user_instance.set_password(password)
                        user_instance.save()
                        description = ""
                        if 'company_about' in request.data:
                            description=request.data['company_about']
                        EmployerProfile.objects.create(
                            user=user_instance, description=description, is_verified=True
                        )
                        email_context["yourname"] = user_instance.name
                        email_context["type"] = 'job'
                        email_context["title"] = request.data['title']
                        email_context["password"] = password
                        email_context["youremail"] = request.data['company_email']
                        email_context['Ctype'] = 'Job'
                        email_context["job_id"] = job_instance.job_id
                        email_context["job_link"] = Common.FRONTEND_BASE_URL + "/jobs/details/" + str(job_instance.slug)
                        email_context["discription"] = process_description(job_instance.description)
                        if user_instance.email:
                            if send_email_automatically == 'False':
                                get_email_object(
                                    subject=f'Koor jobs create account for you',
                                    email_template_name='email-templates/create-account.html',
                                    context=email_context,
                                    to_email=[user_instance.email, ]
                                )
            try:
                serializer.is_valid(raise_exception=True)
                if serializer.update(job_instance, serializer.validated_data):
                    JobDetails.objects.filter(id=jobId).update(user=user_instance)
                    email_context["yourname"] = user_instance.name
                    email_context["type"] = 'job'
                    email_context["title"] = request.data['title']
                    email_context["youremail"] = str(user_instance.email)
                    email_context['Ctype'] = 'Job'
                    email_context["job_id"] = job_instance.job_id
                    email_context["job_link"] = Common.FRONTEND_BASE_URL + "/jobs/details/" + str(job_instance.slug)
                    email_context["discription"] = process_description(job_instance.description)
                    if user_instance.email:
                        if send_email_automatically == 'False':
                            get_email_object(
                                subject=f'Koor Published: ' + str(request.data['title']),
                                email_template_name='email-templates/create-jobs.html',
                                context=email_context,
                                to_email=[user_instance.email, ]
                            )
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


class TenderCreateView(generics.ListAPIView):
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
        try:
            user_instance = None
            send_email_automatically= None
            if 'send_email_automatically' in request.data:
                send_email_automatically = request.data['send_email_automatically']
            if 'employer_id' in request.data:
                employerId = request.data['employer_id']
                user_instance = User.objects.get(id=employerId)
            else:
                if 'company_email' in request.data:
                    if User.objects.filter(email=request.data['company_email']).exists():
                        user_instance = User.objects.get(email=request.data['company_email'])
                    else:
                        user_instance = User.objects.create(
                            role="employer", is_company=True, is_verified=True, is_active=True, 
                            email=request.data['company_email'], name=request.data['company']
                        )
                        password = generate_random_password()
                        user_instance.set_password(password)
                        user_instance.save()
                        description = ""
                        if 'company_about' in request.data:
                            description=request.data['company_about']
                        EmployerProfile.objects.create(
                            user=user_instance, description=description, is_verified=True
                        )
                        email_context["yourname"] = user_instance.name
                        email_context["type"] = 'tender'
                        email_context["title"] = request.data['title']
                        email_context["password"] = password
                        email_context["youremail"] = request.data['company_email']
                        if user_instance.email:
                            if send_email_automatically == 'False':
                                get_email_object(
                                    subject=f'Koor jobs create account for you',
                                    email_template_name='email-templates/create-account.html',
                                    context=email_context,
                                    to_email=[user_instance.email, ]
                                )
                
            serializer = CreateTendersSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            tender_instance = serializer.save(user_instance)
            if user_instance:
                email_context["yourname"] = user_instance.name
                email_context["type"] = 'tender'
                email_context["title"] = request.data['title']
                email_context['Ctype'] = 'Tender'
                email_context["job_id"] = tender_instance.tender_id
                email_context["job_link"] = Common.FRONTEND_BASE_URL + "/tender/details/" + str(tender_instance.slug)
                email_context["discription"] = process_description(tender_instance.description)
                if send_email_automatically == 'False':
                    if user_instance.email:
                        get_email_object(
                            subject=f'Koor Published: ' + str(request.data['title']),
                            email_template_name='email-templates/create-jobs.html',
                            context=email_context,
                            to_email=[user_instance.email, ]
                        )
            context["message"] = "Tender added successfully."
            return response.Response(data=context, status=status.HTTP_201_CREATED)
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

    def put(self, request, tenderId):
        """
        Update an existing tender instance with the provided request data.

        Args:
            - `request`: An instance of the Django Request object.

        Returns:
            An instance of the Django Response object with a JSON-encoded message indicating whether the tender instance
            was updated successfully or not.

        Raises:
            - `Http404`: If the TenderDetails instance with the provided tenderId does not exist.

        Notes:
            This method requires a tenderId to be included in the request data, and will only update the tender if the
            authenticated user matches the user associated with the tender instance. The UpdateTenderSerializers class
            is used to serialize the request data and update the tender instance. If the serializer is invalid or the
            user does not have permission to update the tender instance, an appropriate error response is returned.
        """
        context = dict()
        email_context = dict()
        try:
            tender_instance = TenderDetails.objects.get(id=tenderId)
            serializer = UpdateTenderSerializers(data=request.data, instance=tender_instance, partial=True)
            send_email_automatically= None
            if 'send_email_automatically' in request.data:
                send_email_automatically = request.data['send_email_automatically']
            if 'employer_id' in request.data:
                employerId = request.data['employer_id']
                user_instance = User.objects.get(id=employerId)
                TenderDetails.objects.filter(id=tenderId).update(user=user_instance)
            else:
                if 'company_email' in request.data:
                    if User.objects.filter(email=request.data['company_email']).exists():
                        pass
                    else:
                        user_instance = User.objects.create(
                            role="employer", is_company=True, is_verified=True, is_active=True, 
                            email=request.data['company_email'], name=request.data['company']
                        )
                        password = generate_random_password()
                        user_instance.set_password(password)
                        user_instance.save()
                        description = ""
                        if 'company_about' in request.data:
                            description=request.data['company_about']
                        EmployerProfile.objects.create(
                            user=user_instance, description=description, is_verified=True
                        )
                        email_context["yourname"] = user_instance.name
                        email_context["type"] = 'tender'
                        email_context["title"] = request.data['title']
                        email_context['Ctype'] = 'Tender'
                        email_context["job_id"] = tender_instance.tender_id
                        email_context["job_link"] = Common.FRONTEND_BASE_URL + "/tender/details/" + str(tender_instance.slug)
                        email_context["discription"] = process_description(tender_instance.description)
                        email_context["password"] = password
                        email_context["youremail"] = request.data['company_email']
                        if user_instance.email:
                            if send_email_automatically == 'False':
                                get_email_object(
                                    subject=f'Koor jobs create account for you',
                                    email_template_name='email-templates/create-account.html',
                                    context=email_context,
                                    to_email=[user_instance.email, ]
                                )
            
            try:
                serializer.is_valid(raise_exception=True)
                if serializer.update(tender_instance, serializer.validated_data):
                    TenderDetails.objects.filter(id=tenderId).update(user=user_instance)
                    email_context["yourname"] = str(user_instance.name)
                    email_context["type"] = 'tender'
                    email_context["title"] = request.data['title']
                    email_context['Ctype'] = 'Tender'
                    email_context["job_id"] = tender_instance.tender_id
                    email_context["job_link"] = Common.FRONTEND_BASE_URL + "/tender/details/" + str(tender_instance.slug)
                    email_context["discription"] = process_description(tender_instance.description)
                    email_context["youremail"] = str(user_instance.email)
                    if user_instance.email:
                        if send_email_automatically == 'False':
                            get_email_object(
                                subject=f'Koor Published: ' + str(request.data['title']),
                                email_template_name='email-templates/create-jobs.html',
                                context=email_context,
                                to_email=[user_instance.email, ]
                            )
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
        except TenderDetails.DoesNotExist:
            return response.Response(
                data={"tenderId": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["message"] = str(e)
            return response.Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
            )


class PackageView(generics.ListAPIView):
    """
    A view for displaying a list of resources.

    Attributes:
        - permission_classes ([permissions.IsAuthenticated]): List of permission classes that the view requires. In this
            case, only authenticated users are allowed to access the view.

        - serializer_class (ResourcesSerializers): The serializer class used for data validation and serialization.

        - queryset (QuerySet): The queryset that the view should use to retrieve the countries. By default, it is set
            to retrieve all countries using `Packages.objects.all()`.

        - filter_backends ([filters.SearchFilter]): List of filter backends to use for filtering the queryset. In this
            case, only `SearchFilter` is used.

        - search_fields (list): List of fields to search for in the queryset. In this case, the field is "title".

    """

    permission_classes = [permissions.AllowAny]
    serializer_class = PackageSerializers
    queryset = Packages.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    pagination_class = CustomPagination

    def list(self, request):
        if self.get_queryset().exists():
            pass
        else:
            run_seed()
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def patch(self, request):
        """
        Update multiple Packages objects based on the data received in the PATCH request.

        Args:
            request (HttpRequest): The HTTP request object containing the data to update.

        Returns:
            Response: A Response object indicating the status of the update operation.

        Description:
        This function is used to update multiple Packages objects in the database based on the data received
        in the PATCH request. The request should contain a list of packages in JSON format, and each package
        should have an 'id' field that matches the primary key of the corresponding Packages object.

        The 'request' object should contain the list of packages under the 'data' key. Each package in the list
        should have fields representing the properties that need to be updated. The function iterates over the
        list of packages, retrieves the corresponding Packages object from the database using the 'id' field,
        and then updates the object with the new data provided in the request.

        If a package with a given 'id' is not found in the database, an error message is added to the 'error_message'
        list. After processing all the packages, if any errors were encountered, the function returns a Response
        object with status code 400 and a JSON object containing the error messages. Otherwise, it returns a Response
        object with status code 200 and a JSON object indicating that the packages were updated successfully.

        Note:
        - The 'Packages' model should be defined in the Django app for this function to work correctly.
        - The 'request' object should contain a list of packages under the key 'data'.
        - Each package in the list should have an 'id' field that corresponds to the primary key of the Packages model.
        - The 'benefit', 'price', and 'credit' fields are updated only if the corresponding fields are present in the
        package.

        Example:
        If you send a PATCH request to this view with the following JSON data:
        {
            "data": [
                {"id": "53735375-e684-4426-ab34-d2e4d8243393", "benefit": "New Benefit"},
                {"id": "b5b6a35f-9153-4549-b6f8-649023a45843", "price": "9.99"}
            ]
        }

        It will update the 'benefit' field for the object with 'id' 53735375-e684-4426-ab34-d2e4d8243393 and
        the 'price' field for the object with 'id' b5b6a35f-9153-4549-b6f8-649023a45843. If any of the provided 'id's
        are not found in the database, it will return a response with the error message for the corresponding 'id'.

        """
        
        context = dict()
        error_message = []
        package_list = request.data  # Directly access the list from request.data
        for data in package_list:
            obj_id = UUID(data["id"])
            try:
                obj = Packages.objects.get(id=obj_id)
                if data['benefit']:
                    obj.benefit = data["benefit"]
                if data['price']:
                    obj.price = data["price"]
                if data['credit']:
                    obj.credit = data["credit"]
                obj.save()
            except Packages.DoesNotExist:
                error_message.append(str(obj_id) + ' does not exist.')
        if error_message:
            context["message"] = error_message
            return response.Response(
                    data=context,
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            context["message"] = 'Packages update successfully.'
            return response.Response(
                data=context,
                status=status.HTTP_200_OK
            )


class GenerateInvoiceView(generics.ListAPIView):
    """
    A view for generating a list of invoices with advanced filtering and searching capabilities.

    This view extends the generics.ListAPIView and provides the functionality to retrieve a list of invoices while
    allowing filtering, searching, and pagination.

    Attributes:
        serializer_class (class): The serializer class responsible for converting Invoice objects into JSON
                                representation.
        permission_classes (list): A list of permission classes that restrict access to this view, ensuring only
                                authenticated users can access it.
        queryset (QuerySet): The base queryset containing all Invoice objects, ordered by creationdate in descending
                                order.
        filter_backends (list): A list of filter backend classes responsible for applying various filtering options to
                                the queryset.
        filterset_class (class): The class defining the filter fields and lookup options for filtering the queryset
                                based on specific parameters.
        search_fields (list): A list of field names that can be searched using a search term, enabling search
                                functionality on the view.
        pagination_class (class): The pagination class determining how the list of invoices should be paginated in the
                                response.

    Note:
        - This view is designed to be accessed by authenticated users only.
        - Invoices are retrieved in descending order based on their creation date.
        - Filtering options are available, allowing users to narrow down the list of invoices.
        - Search functionality is provided for searching invoices by user's name.
        - Pagination is applied to the response using the specified pagination class.
    """

    serializer_class = InvoiceSerializers
    permission_classes = [permissions.IsAuthenticated]
    queryset = Invoice.objects.all().order_by('-created')
    filter_backends = [filters.SearchFilter, django_filters.DjangoFilterBackend]
    filterset_class = InvoiceDetailsFilter
    search_fields = [
        'user__name',
    ]
    pagination_class = CustomPagination

    def list(self, request):
        """
        Retrieve a list of records based on filtering criteria.

        This function is used to retrieve a list of records that match the filtering criteria provided in the request
        parameters. The function is accessible only to staff users.

        Args:
            self: The instance of the view.
            request: The HTTP request object.
            userId (int): The ID of the user for whom the records are to be retrieved.

        Returns:
            Response: An HTTP response object containing the serialized data of the retrieved records or an error
                    message if the request is not authorized or if the specified user does not exist.

        Raises:
            User.DoesNotExist: If the specified user does not exist.

        """
        
        context = dict()
        
        # Check if the requesting user is a staff member
        if self.request.user.is_staff:
            queryset = self.filter_queryset(self.get_queryset())
            userId = self.request.GET.get('userId', None)
            invoiceId = self.request.GET.get('invoiceId', None)
            if invoiceId:
                queryset = queryset.filter(invoice_id=invoiceId)
            if userId:
                try:
                    user_instance = User.objects.get(id=userId)
                    queryset = queryset.filter(user=user_instance)
                except User.DoesNotExist:
                    return response.Response(data={"userId": "Does Not Exist"}, status=status.HTTP_404_NOT_FOUND)
                            
            # Retrieve start_date and end_date from request parameters
            start_date = self.request.GET.get('from', None)
            
            # Check if start_date is missing
            if start_date == None:
                context['message'] = "Please enter from."
                return response.Response(
                    data=context,
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            end_date = self.request.GET.get('to', datetime.now())
            end_date = datetime.strptime(str(end_date), '%Y-%m-%d')
            end_date = datetime.combine(end_date.date(), time(hour=23, minute=59, second=59))
            # Apply filtering based on start_date and end_date
            is_send = self.request.GET.get('send', None)
            if start_date:
                if is_send:
                    if is_send == "true" or is_send == "True":
                        is_send = True
                    else:
                        is_send = False
                    queryset = queryset.filter(
                        created__gte=start_date,
                        created__lte=end_date,
                        is_send=bool(is_send)
                    )
                else:
                    queryset = queryset.filter(
                        created__gte=start_date,
                        created__lte=end_date
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

class InvoiceDetailView(generics.GenericAPIView):
    """
    A view to retrieve detailed information about an invoice.

    This view retrieves detailed information about an invoice based on the provided `invoiceId`.
    It requires the user to be authenticated and have staff privileges to access the information.
    If the user is authorized, the detailed information of the invoice is serialized and returned.
    If the user lacks proper authorization, an appropriate error message is returned.

    Attributes:
        serializer_class (Serializer): The serializer class used to serialize the invoice data.
        permission_classes (list): The list of permission classes required for accessing this view.

    Methods:
        get(request, invoiceId):
        Retrieve detailed information about the specified invoice.

        Args:
            request (HttpRequest): The HTTP request object.
            invoiceId (int): The ID of the invoice to retrieve information for.

        Returns:
            Response: An HTTP response containing serialized invoice data if successful, or an error message with an
                        appropriate status code if unsuccessful.
    """

    serializer_class = InvoiceDetailSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, invoiceId):
        """
        Retrieve detailed information about the specified invoice.

        Args:
            request (HttpRequest): The HTTP request object.
            invoiceId (int): The ID of the invoice to retrieve information for.

        Returns:
            Response: An HTTP response containing serialized invoice data if successful, or an error message with an
                        appropriate status code if unsuccessful.
        """
        
        context = dict()
        if self.request.user.is_staff:
            try:
                if invoiceId:
                    invoice_data = Invoice.objects.get(invoice_id=invoiceId)
                    get_data = self.serializer_class(invoice_data)
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
        else:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
            )


def GenerateInvoice():
    """
    Generates invoices for eligible employers based on recharge history within the previous month.

    This function calculates the first and last days of the previous month, then retrieves recharge history data for
    eligible employers within that time frame. For each employer, it calculates the total recharge amount, points
    earned, and applicable discount. An invoice is created for each employer with relevant details.

    Returns:
        HttpResponse: A response indicating successful invoice generation.

    Usage:
        Call this function to generate invoices for eligible employers based on their recharge history within the
        previous month.

    Notes:
        - Requires the 'User' and 'RechargeHistory' models to be defined and accessible in the current scope.
        - The current implementation focuses on generating invoices for employers on the first day of the current month.
        If executed on other days, the function won't generate invoices.

    Example:
        GenerateInvoice()
    """

    # Get the current date
    current_date = datetime.now()

    # Calculate the first day of the current month
    first_day_of_current_month = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Calculate the last day of the last month
    last_day_of_last_month = first_day_of_current_month - timedelta(days=1)

    # Calculate the first day of the last month
    first_day_of_last_month = last_day_of_last_month.replace(day=1)

    # Calculate the end date of the last month
    end_date_of_last_month = last_day_of_last_month.replace(hour=23, minute=59, second=59)

    # Format the dates
    start_date_formatted = first_day_of_last_month.strftime('%Y-%m-%d %H:%M:%S')
    end_date_formatted = end_date_of_last_month.strftime('%Y-%m-%d %H:%M:%S')
    start_date = first_day_of_last_month.strftime('%Y-%m-%d')
    end_date = end_date_of_last_month.strftime('%Y-%m-%d')

    # Check if the current date is the first day of the month
    if current_date.date() == first_day_of_current_month.date():
        user_data = User.objects.filter(role='employer')
        for user_instance in user_data:
            recharge_history_data = RechargeHistory.objects.filter(
                user=user_instance, created__gte=start_date_formatted, created__lte=end_date_formatted
            )
            if recharge_history_data:
                total = 0
                discount = 0
                points = 0
                for recharge_history in recharge_history_data:
                    total = total + recharge_history.amount
                    points = points + recharge_history.points
                discount = total
                grand_total = total - discount
                if Invoice.objects.filter(user=user_instance, start_date=start_date, end_date=end_date).exists():
                    pass
                else:
                    invoice_instance = Invoice.objects.create(
                        start_date=start_date, end_date=end_date, total=total, 
                        discount=discount, grand_total=grand_total, points=points,
                        user=user_instance
                    )
                    if invoice_instance.invoice_id:
                        # Retrieve invoice data from the database
                        invoice_data = Invoice.objects.get(invoice_id=invoice_instance.invoice_id)
                        if invoice_instance.start_date:
                            invoice_month = calendar.month_name[invoice_instance.start_date.month]
                        else:
                            invoice_month = calendar.month_name[invoice_instance.created.month]
                        email_context["invoice_month"] = invoice_month
                        user_email = []

                        # Get the user's email address
                        if invoice_data.user:
                            if invoice_data.user.email:
                                user_email.append(invoice_data.user.email)

                        if user_email:
                            email_context = dict()

                            # Determine user name for email context
                            if invoice_data.user:
                                if invoice_data.user.name:
                                    user_name = invoice_data.user.name
                                else:
                                    user_name = user_email[0]
                            elif invoice_data.company:
                                user_name = invoice_data.company
                            else:
                                user_name = user_email[0]

                            # Populate email context
                            # email_context["invoice_month"] = invoice_month
                            # Send the email
                            pdf = generate_pdf_file(invoice_instance.invoice_id)
                            get_email_object(
                                subject=f'Mail for Invoice',
                                email_template_name='email-templates/mail-for-invoice.html',
                                context=email_context,
                                to_email=user_email,
                                type="attachment",
                                filename="Invoice.pdf", 
                                file=pdf
                            )
                            Invoice.objects.filter(invoice_id=invoice_instance.invoiceId).update(is_send=True)
    return HttpResponse("Invoice Generated")


class InvoiceSendView(generics.GenericAPIView):
    """
    A view to send an invoice via email to a user.

    This view is used to send an invoice to a user's email address. It checks if the requesting user
    is a staff member, retrieves the specified invoice data, and sends an email containing the invoice
    information. If successful, a success message is returned; otherwise, an error message is returned.

    Requires authentication.

    Attributes:
        permission_classes (list): A list of permission classes that define the access permissions
            for this view. Requires the requesting user to be authenticated.

    Methods:
        get(request, invoiceId):
            Send the invoice via email to the user associated with the invoice.

    Raises:
        Exception: If an error occurs during the process of sending the invoice.

    Returns:
        Response: A response indicating the outcome of the operation, along with a message.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, invoiceId):
        """
        Send the invoice via email to the user associated with the invoice.

        Args:
            request (HttpRequest): The HTTP request object.
            invoiceId (int): The ID of the invoice to be sent.

        Returns:
            Response: A response indicating the outcome of the operation, along with a message.
        """
        context = dict()
        email_context = dict()
        if self.request.user.is_staff:
            try:
                if invoiceId:
                    # Retrieve invoice data from the database
                    invoice_data = Invoice.objects.get(invoice_id=invoiceId)
                    if invoice_data.start_date:
                        invoice_month = calendar.month_name[invoice_data.start_date.month]
                    else:
                        invoice_month = calendar.month_name[invoice_data.created.month]
                    email_context["invoice_month"] = invoice_month
                    user_email = []

                    # Get the user's email address
                    if invoice_data.user:
                        if invoice_data.user.email:
                            user_email.append(invoice_data.user.email)

                    if user_email:
                        # Determine user name for email context
                        if invoice_data.user:
                            if invoice_data.user.name:
                                user_name = invoice_data.user.name
                            else:
                                user_name = user_email[0]
                        elif invoice_data.company:
                            user_name = invoice_data.company
                        else:
                            user_name = user_email[0]

                        # Populate email context
                        # email_context["invoice_month"] = invoice_month
                        # Send the email
                        pdf = generate_pdf_file(invoiceId)
                        get_email_object(
                            subject=f'Mail for Invoice',
                            email_template_name='email-templates/mail-for-invoice.html',
                            context=email_context,
                            to_email=user_email,
                            type="attachment",
                            filename="Invoice.pdf", 
                            file=pdf
                        )
                        Invoice.objects.filter(invoice_id=invoiceId).update(is_send=True)
                context["message"] = "Invoice sent successfully."
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
        else:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
            )


class DownloadInvoiceView(generics.GenericAPIView):
    """
    A view class that generates and serves PDF invoices for download based on invoice ID.

    This view is intended for allowing anyone (with or without authentication) to download PDF invoices
    corresponding to a specified invoice ID. It fetches invoice details, user information, and recharge history,
    then generates a PDF representation of the invoice using an HTML template.

    Attributes:
        permission_classes (list): A list of permission classes that control access to this view. In this case,
                                  it allows any user to access the view.

    Methods:
        get(self, request): Processes the GET request, generates the PDF invoice, and serves it as a response.

    Usage:
        Make a GET request to this view with the 'invoice-id' parameter in the query string to download the
        corresponding invoice PDF.
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """
        Generate and serve a PDF invoice for download.

        This method handles the GET request to generate a PDF invoice based on the specified 'invoice-id' parameter.
        It retrieves invoice data, user information, recharge history, and SMTP settings. Then, it generates a PDF
        using an HTML template and serves it as an HTTP response.

        Args:
            request (HttpRequest): The HTTP GET request object.

        Returns:
            HttpResponse: An HTTP response containing the generated PDF invoice with 'application/pdf' content type.
        """

        context = dict()
        downloaded_file = ""
        if 'invoice-id' in request.GET:
            Page_title = "KOOR INVOICE"
            invoice_data = Invoice.objects.get(invoice_id=request.GET['invoice-id'])
            if invoice_data.start_date:
                invoice_month = calendar.month_name[invoice_data.start_date.month]
            else:
                invoice_month = calendar.month_name[invoice_data.created.month]
            smtp_setting = SMTPSetting.objects.last()
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
            invoice_icons = InvoiceIcon.objects.all()
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
            file_response = html_to_pdf(
                'email-templates/pdf-invoice.html', {
                    'pagesize': 'A4', 'invoice_data': invoice_data, 'Page_title': Page_title,
                    'invoice_month':invoice_month, 'LOGO': Common.BASE_URL + smtp_setting.logo.url,
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
                    'mobile_number':new_mobile_number, 'history_data':history_data
                }
            )
            return file_response
        else:
            context['message'] = "Invoice id is required"
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
            )

  
class GoogleAddSenseCodeView(generics.ListAPIView):
    
    permission_classes = [permissions.AllowAny]
    serializer_class = GoogleAddSenseCodeSerializers
    queryset = GoogleAddSenseCode.objects.all().order_by('created')

    def list(self, request):
        page_title = request.GET.get('page_title', None)
        if page_title:
            queryset = self.filter_queryset(self.get_queryset().filter(page_title=page_title))
        else:
            queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def post(self, request):
        
        context = dict()
        serializer = self.serializer_class(data=request.data)
        try:
            if self.request.user.is_staff:
                serializer.is_valid(raise_exception=True)
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

    def put(self, request, codeId):
        
        context = dict()
        try:
            code_instance = GoogleAddSenseCode.objects.get(id=codeId)
            serializer = self.serializer_class(data=request.data, instance=code_instance, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                if serializer.update(code_instance, serializer.validated_data):
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
        except GoogleAddSenseCode.DoesNotExist:
            return response.Response(
                data={"codeId": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            context["message"] = e
            return response.Response(
                data=context,
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, codeId):
        
        context = dict()
        if self.request.user.is_staff:
            try:
                GoogleAddSenseCode.objects.get(id=codeId).delete()
                context['message'] = "Deleted Successfully"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except GoogleAddSenseCode.DoesNotExist:
                return response.Response(
                    data={"codeId": "Does Not Exist"},
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


class FinancialCountView(generics.GenericAPIView):

    permission_classes = [permissions.AllowAny]
    serializer_class = FinancialCountSerializers

    def get(self, request):
        context = dict()
        response_context = dict()
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
                end_date = datetime.strptime(str(end_date), '%Y-%m-%d')
                end_date = datetime.combine(end_date.date(), time(hour=23, minute=59, second=59))
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
                serializer = self.get_serializer(queryset, context=context)
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



class ManageUserRightsView(generics.GenericAPIView):

    serializer_class = ModifyUserRightsSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        response_context = dict()
        user_id = request.GET.get('userId', self.request.user.id)
        try:
            user_instance = User.objects.get(id=user_id)
            if user_instance.role == "admin":
                rights_data = UserRights.objects.filter(is_removed=False).annotate(
                    has_subrights=Exists(UserSubRights.objects.filter(rights_id=OuterRef('id')))
                ).filter(has_subrights=True)
                get_data = UserRightsSerializers(rights_data, many=True, context={'user': user_instance})
                return response.Response(
                    data=get_data.data,
                    status=status.HTTP_200_OK
                )
            else:
                response_context['message'] = "This user has no permission to perform this action."
                return response.Response(
                    data=response_context,
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except User.DoesNotExist:
            return response.Response(
                data={"userId": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request):

        response_context = dict()
        user_id = request.GET.get('userId', self.request.user.id)
        try:
            user_instance = User.objects.get(id=user_id)
            if user_instance.role == "admin":
                serializer = self.serializer_class(data=request.data)
                try:
                    serializer.is_valid(raise_exception=True)
                    serializer.save(user=user_instance)
                    response_context['message'] = "Rights Updated Successfully"
                    return response.Response(
                        data=response_context,
                        status=status.HTTP_200_OK
                    )
                except serializers.ValidationError:
                    return response.Response(
                        data=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                response_context['message'] = "This user has no permission to perform this action."
                return response.Response(
                    data=response_context,
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except User.DoesNotExist:
            return response.Response(
                data={"userId": "Does Not Exist"},
                status=status.HTTP_404_NOT_FOUND
            )    


class AdminListView(generics.ListAPIView):

    permission_classes = [permissions.AllowAny]
    serializer_class = AdminSerializer
    queryset = User.objects.filter(role='admin')
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email']
    pagination_class = CustomPagination

    def list(self, request):
        if self.request.user.id:
            queryset = self.filter_queryset(self.get_queryset().exclude(id=self.request.user.id))
        else:
            queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)


class CityTitleModifyView(generics.GenericAPIView):

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        string = request.GET.get('title', None)
        if string:
            capitalized_string = string.title()
            City.objects.filter(title=string).update(title=capitalized_string)
        return response.Response(
            data={"message":"title updated"},
            status=status.HTTP_200_OK
        )


class GenerateMergedInvoiceView(generics.GenericAPIView):
    
    serializer_class = InvoiceDetailSerializers
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        
        context = dict()
        if self.request.user.is_staff:
            try:
                if 'invoiceId' in request.data:
                    invoice_list = request.data.getlist('invoiceId')
                    invoices = Invoice.objects.filter(invoice_id__in=invoice_list)
                    employer_list = []
                    for get_invoices in invoices:
                        if get_invoices.user in employer_list:
                            pass
                        else:
                            employer_list.append(get_invoices.user)
                    email_context = dict()
                    for employer_data in employer_list:
                        today_date = date.today()
                        direct_url = 'media/invoice/pdf'
                        directry_path_check = pathlib.Path(direct_url)
                        date_folder = str(today_date.day) + "_" + str(today_date.month) + "_" + str(today_date.year)

                        if directry_path_check.exists():
                            direct_url = direct_url + "/" + date_folder
                            directry_path_check = pathlib.Path(direct_url)
                            if directry_path_check.exists():
                                direct_url = direct_url
                            else:
                                os.makedirs(direct_url)
                                direct_url = direct_url

                        else:
                            os.makedirs('media/invoice/pdf')
                            direct_url = 'media/invoice/pdf' + "/" + date_folder
                            os.makedirs(direct_url)
                            direct_url = direct_url
                        if employer_data.name:
                            pdf_name = employer_data.name
                        else:
                            fragments = str(employer_data.email).split("@")  # Split the text with "@"

                            # Remove "." from each fragment and join them with "@"
                            pdf_name = fragments[0].replace(".", "")
                        file_name = direct_url + "/" + str(pdf_name)+ ".pdf"
                        if os.path.exists(file_name):
                            os.remove(file_name)
                        # ---------------------------------------------
                        invoices = Invoice.objects.filter(invoice_id__in=invoice_list).filter(user=employer_data).order_by('created')
                        
                        email_context["yourname"] = employer_data.name
                        email_context["type"] = 'invoice'
                        email_context['Ctype'] = 'Invoice'
                        email_context["invoice_month"] = calendar.month_name[datetime.now().month]
                        if employer_data.email:                    
                            pdf = generate_merge_pdf_file(invoice_list, employer_data)
                            get_email_object(
                                subject=f'Mail for Invoice',
                                email_template_name='email-templates/mail-for-invoice.html',
                                context=email_context,
                                to_email=[employer_data.email, ],
                                type="attachment",
                                filename="Invoice.pdf", 
                                file=pdf
                            )
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
        else:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
            )


class DownloadMergedInvoiceView(generics.GenericAPIView):
    
    serializer_class = InvoiceDetailSerializers
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        
        context = dict()
        if self.request.user.is_staff:
            try:
                if 'invoiceId' in request.data:
                    invoice_list = request.data.getlist('invoiceId')
                    invoices = Invoice.objects.filter(invoice_id__in=invoice_list)
                    employer_list = []
                    for get_invoices in invoices:
                        if get_invoices.user in employer_list:
                            pass
                        else:
                            employer_list.append(get_invoices.user)
                    pdf_context = dict()
                    for employer_data in employer_list:
                        invoices = Invoice.objects.filter(invoice_id__in=invoice_list).filter(user=employer_data).order_by('created')
                        pdf = generate_merge_pdf_file(invoice_list, employer_data)
                        today_date = date.today()
                        direct_url = 'media/invoice/pdf'
                        directry_path_check = pathlib.Path(direct_url)
                        date_folder = str(today_date.day) + "_" + str(today_date.month) + "_" + str(today_date.year)

                        if directry_path_check.exists():
                            direct_url = direct_url + "/" + date_folder
                            directry_path_check = pathlib.Path(direct_url)
                            if directry_path_check.exists():
                                direct_url = direct_url
                            else:
                                os.makedirs(direct_url)
                                direct_url = direct_url

                        else:
                            os.makedirs('media/invoice/pdf')
                            direct_url = 'media/invoice/pdf' + "/" + date_folder
                            os.makedirs(direct_url)
                            direct_url = direct_url
                        if employer_data.name:
                            pdf_name = employer_data.name
                        else:
                            fragments = str(employer_data.email).split("@")  # Split the text with "@"

                            # Remove "." from each fragment and join them with "@"
                            pdf_name = fragments[0].replace(".", "")
                        file_name = direct_url + "/" + str(pdf_name)+ ".pdf"
                        pdf_context[pdf_name] = Common.BASE_URL + "/" + file_name
                        with open(file_name, 'wb') as f:
                            f.write(pdf)
                return response.Response(
                    data=pdf_context,
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                context["message"] = str(e)
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


