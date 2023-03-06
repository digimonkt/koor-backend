from datetime import datetime

from rest_framework import (
    status, generics, serializers,
    response, permissions, filters
)

from core.middleware import JWTMiddleware

from users.models import UserSession

from jobs.models import (
    JobCategory
)
from project_meta.models import (
    Country, City, EducationLevel,
    Language, Skill, Tag
)

from .models import Content
from .serializers import (
    CountrySerializers, CitySerializers, JobCategorySerializers,
    EducationLevelSerializers, LanguageSerializers, SkillSerializers,
    TagSerializers, ChangePasswordSerializers, ContentSerializers
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
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CountrySerializers
    queryset = Country.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return response.Response({'results': serializer.data})

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

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CitySerializers
    queryset = City.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def list(self, request):
        country_id = request.GET.get('countryId', None)
        queryset = City.objects.all()
        if country_id:
            queryset = City.objects.filter(country_id=country_id)
        queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response({'results': serializer.data})

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

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = JobCategorySerializers
    queryset = JobCategory.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return response.Response({'results': serializer.data})

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

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EducationLevelSerializers
    queryset = EducationLevel.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return response.Response({'results': serializer.data})

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

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LanguageSerializers
    queryset = Language.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return response.Response({'results': serializer.data})

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

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SkillSerializers
    queryset = Skill.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def list(self, request):
        exclude = request.GET.get('exclude', None)
        if exclude:
            queryset = self.filter_queryset(self.get_queryset().exclude(title__in=exclude.split(",")))
        else:
            queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return response.Response({'results': serializer.data})

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

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TagSerializers
    queryset = Tag.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return response.Response({'results': serializer.data})

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
                    instance.is_removed=False
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
                    instance.is_removed=False
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
            