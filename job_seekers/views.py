from django.shortcuts import get_object_or_404
from rest_framework import (
    generics, response, status,
    permissions, serializers
)

from jobs.models import JobDetails
from user_profile.models import JobSeekerProfile
from users.models import User

from .models import (
    EducationRecord, EmploymentRecord, JobSeekerLanguageProficiency,
    JobSeekerSkill, AppliedJob
)
from .serializers import (
    UpdateAboutSerializers, EducationSerializers, JobSeekerLanguageProficiencySerializers,
    EmploymentRecordSerializers, JobSeekerSkillSerializers, AppliedJobSerializers
)


class UpdateAboutView(generics.GenericAPIView):
    """
    A view for updating the JobSeekerProfile of the currently authenticated User.

    Attributes:
        serializer_class: The serializer class to use for updating the JobSeekerProfile.
        permission_classes: The permission classes required to access this view.

    Methods:
        patch: Handle PATCH requests to update the JobSeekerProfile of the authenticated User.

    Returns:
        A Response object with a success or error message, and an appropriate status code.
    """

    serializer_class = UpdateAboutSerializers
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        context = dict()
        if self.request.user.role == "job_seeker":
            profile_instance = get_object_or_404(JobSeekerProfile, user=request.user)
            serializer = self.serializer_class(data=request.data, instance=profile_instance, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                if 'email' in serializer.validated_data:
                    if User.objects.filter(email=serializer.validated_data['email']).exists():
                        if profile_instance.user.email != serializer.validated_data['email']:
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


class EducationsView(generics.GenericAPIView):
    """
    A generic API view for handling education records.

    Attributes:
        - `permission_classes (list)`: The list of permission classes that the user must have to access this view.
                                In this case, only authenticated users can access this view.

        - `serializer_class (EducationSerializers)`: The serializer class that the view uses to serialize and
                                                deserialize the EducationRecord model.

    Returns:
        Serialized education records in JSON format, with authentication required to access the view. 
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EducationSerializers

    def post(self, request):
        """
        Handles HTTP POST requests for creating a new education record.

        Args:
            request (HttpRequest): The request object sent to the server.

        Returns:
            HTTP response with serialized data in JSON format, and status codes indicating whether the request was
            successful or not.

        Raises:
            serializers.ValidationError: If the data in the request is invalid or incomplete.

            Exception: If an error occurs while processing the request.

        Notes:
            This function creates a new education record using the serializer class specified in the `serializer_class`
            attribute of the view. The serializer is first validated and then saved to the database. The `user` field
            of the education record is set to the currently logged-in user.
            If the serializer is not valid, a `serializers.ValidationError` is raised and a response with a status code
            of 400 is returned. If any other error occurs, a response with a status code of 400 is returned along with
            an error message in the `message` field of the response data. If the serializer is valid and the record is
            successfully created, a response with the serialized data and a status code of 201 is returned.
        """

        context = dict()
        if request.user.role == "job_seeker":
            serializer = self.serializer_class(data=request.data)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save(user=request.user)
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
        else:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
            )

    def patch(self, request, educationId):
        """
        Update an `EducationRecord` instance for a `job seeker`.

        Args:
            - `request`: The HTTP request object.
            - `educationId`: The ID of the `EducationRecord` instance to update.

        Returns:
            - A Response object with a message and HTTP status code indicating the result of the update.

        Raises:
            - `ValidationError`: If the request data is not valid.
            - `NotFound`: If the EducationRecord instance does not exist.
            - `Exception`: If an error occurs during the update.

        Note:
            - This function is only accessible to job seekers. If the user has a role other than `'job_seeker'`, an
            error message is returned indicating that the user does not have permission to perform the action.
        """
        context = dict()
        if request.user.role == "job_seeker":
            try:
                education_instance = EducationRecord.objects.get(id=educationId, user=request.user)
                serializer = self.serializer_class(data=request.data, instance=education_instance, partial=True)
                try:
                    serializer.is_valid(raise_exception=True)
                    if serializer.update(education_instance, serializer.validated_data):
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
            except EducationRecord.DoesNotExist:
                return response.Response(
                    data={"education record": "Does Not Exist"},
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                context["message"] = e
                return response.Response(
                    data=context,
                    status=status.HTTP_404_NOT_FOUND
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

    def delete(self, request, educationId):
        """
        Deletes an EducationRecord object with the given ID if the authenticated user is a job seeker and owns the
        EducationRecord.
        Args:
            request: A DRF request object.
            educationId: An integer representing the ID of the EducationRecord to be deleted.
        Returns:
            A DRF response object with a success or error message and appropriate status code.
        """
        context = dict()
        if request.user.role == "job_seeker":
            try:
                EducationRecord.objects.get(id=educationId, user=request.user).delete()
                context['message'] = "Deleted Successfully"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except EducationRecord.DoesNotExist:
                return response.Response(
                    data={"education record": "Does Not Exist"},
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


class LanguageView(generics.GenericAPIView):
    """
    A generic API view for handling JobSeekerLanguageProficiency.

    Attributes:
        - `permission_classes (list)`: The list of permission classes that the user must have to access this view.
                                In this case, only authenticated users can access this view.

        - `serializer_class (JobSeekerLanguageProficiencySerializers)`: The serializer class that the view uses to
                                                serialize and deserialize the JobSeekerLanguageProficiency model.

    Returns:
        Serialized JobSeekerLanguageProficiencys in JSON format, with authentication required to access the view.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = JobSeekerLanguageProficiencySerializers

    def post(self, request):
        """
        Handles HTTP POST requests for creating a new JobSeekerLanguageProficiency.

        Args:
            request (HttpRequest): The request object sent to the server.

        Returns:
            HTTP response with serialized data in JSON format, and status codes indicating whether the request was
            successful or not.

        Raises:
            serializers.ValidationError: If the data in the request is invalid or incomplete.

            Exception: If an error occurs while processing the request.

        Notes:
            This function creates a new JobSeekerLanguageProficiency using the serializer class specified in the `serializer_class`
            attribute of the view. The serializer is first validated and then saved to the database. The `user` field
            of the JobSeekerLanguageProficiency is set to the currently logged-in user.
            If the serializer is not valid, a `serializers.ValidationError` is raised and a response with a status code
            of 400 is returned. If any other error occurs, a response with a status code of 400 is returned along with
            an error message in the `message` field of the response data. If the serializer is valid and the record is
            successfully created, a response with the serialized data and a status code of 201 is returned.
        """

        context = dict()
        if request.user.role == "job_seeker":
            serializer = self.serializer_class(data=request.data)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save(user=request.user)
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
        else:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
            )

    def patch(self, request, languageId):
        """
        Update an `JobSeekerLanguageProficiency` instance for a `job seeker`.

        Args:
            - `request`: The HTTP request object.
            - `languageId`: The ID of the `JobSeekerLanguageProficiency` instance to update.

        Returns:
            - A Response object with a message and HTTP status code indicating the result of the update.

        Raises:
            - `ValidationError`: If the request data is not valid.
            - `NotFound`: If the JobSeekerLanguageProficiency instance does not exist.
            - `Exception`: If an error occurs during the update.

        Note:
            - This function is only accessible to job seekers. If the user has a role other than `'job_seeker'`, an
            error message is returned indicating that the user does not have permission to perform the action.
        """
        context = dict()
        if request.user.role == "job_seeker":
            try:
                language_instance = JobSeekerLanguageProficiency.objects.get(id=languageId, user=request.user)
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
            except JobSeekerLanguageProficiency.DoesNotExist:
                return response.Response(
                    data={"job_seeker_language_proficiency": "Does Not Exist"},
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                context["message"] = e
                return response.Response(
                    data=context,
                    status=status.HTTP_404_NOT_FOUND
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

    def delete(self, request, languageId):
        """
        Deletes an JobSeekerLanguageProficiency object with the given ID if the authenticated user is a
        job seeker and owns the JobSeekerLanguageProficiency.
        Args:
            request: A DRF request object.
            languageId: An integer representing the ID of the JobSeekerLanguageProficiency to be deleted.
        Returns:
            A DRF response object with a success or error message and appropriate status code.
        """
        context = dict()
        if request.user.role == "job_seeker":
            try:
                JobSeekerLanguageProficiency.objects.get(id=languageId, user=request.user).delete()
                context['message'] = "Deleted Successfully"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except JobSeekerLanguageProficiency.DoesNotExist:
                return response.Response(
                    data={"job_seeker_language_proficiency": "Does Not Exist"},
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


class WorkExperiencesView(generics.GenericAPIView):
    """
    A generic API view for handling employment record.

    Attributes:
        - `permission_classes (list)`: The list of permission classes that the user must have to access this view.
                                In this case, only authenticated users can access this view.

        - `serializer_class (EmploymentRecordSerializers)`: The serializer class that the view uses to serialize and
                                                deserialize the EmploymentRecord model.

    Returns:
        Serialized employment record in JSON format, with authentication required to access the view. 
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmploymentRecordSerializers

    def post(self, request):
        """
        Handles HTTP POST requests for creating a new employment record.

        Args:
            request (HttpRequest): The request object sent to the server.

        Returns:
            HTTP response with serialized data in JSON format, and status codes indicating whether the request was
            successful or not.

        Raises:
            serializers.ValidationError: If the data in the request is invalid or incomplete.

            Exception: If an error occurs while processing the request.

        Notes:
            This function creates a new employment record using the serializer class specified in the `serializer_class`
            attribute of the view. The serializer is first validated and then saved to the database. The `user` field
            of the employment record is set to the currently logged-in user.
            If the serializer is not valid, a `serializers.ValidationError` is raised and a response with a status code
            of 400 is returned. If any other error occurs, a response with a status code of 400 is returned along with
            an error message in the `message` field of the response data. If the serializer is valid and the record is
            successfully created, a response with the serialized data and a status code of 201 is returned.
        """

        context = dict()
        if request.user.role == "job_seeker":
            serializer = self.serializer_class(data=request.data)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save(user=request.user)
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
        else:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
            )

    def patch(self, request, workExperienceId):
        """
        Update an `EmploymentRecord` instance for a `job seeker`.

        Args:
            - `request`: The HTTP request object.
            - `workExperienceId`: The ID of the `EmploymentRecord` instance to update.

        Returns:
            - A Response object with a message and HTTP status code indicating the result of the update.

        Raises:
            - `ValidationError`: If the request data is not valid.
            - `NotFound`: If the EmploymentRecord instance does not exist.
            - `Exception`: If an error occurs during the update.

        Note:
            - This function is only accessible to job seekers. If the user has a role other than `'job_seeker'`, an
            error message is returned indicating that the user does not have permission to perform the action.
        """
        context = dict()
        if request.user.role == "job_seeker":
            try:
                employment_instance = EmploymentRecord.objects.get(id=workExperienceId, user=request.user)
                serializer = self.serializer_class(data=request.data, instance=employment_instance, partial=True)
                try:
                    serializer.is_valid(raise_exception=True)
                    if serializer.update(employment_instance, serializer.validated_data):
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
            except EmploymentRecord.DoesNotExist:
                return response.Response(
                    data={"employment_record": "Does Not Exist"},
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                context["message"] = e
                return response.Response(
                    data=context,
                    status=status.HTTP_404_NOT_FOUND
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

    def delete(self, request, workExperienceId):
        """
        Deletes an EmploymentRecord object with the given ID if the authenticated user is a job seeker and owns the
        EmploymentRecord.
        Args:
            request: A DRF request object.
            workExperienceId: An integer representing the ID of the EmploymentRecord to be deleted.
        Returns:
            A DRF response object with a success or error message and appropriate status code.
        """
        context = dict()
        if request.user.role == "job_seeker":
            try:
                EmploymentRecord.objects.get(id=workExperienceId, user=request.user).delete()
                context['message'] = "Deleted Successfully"
                return response.Response(
                    data=context,
                    status=status.HTTP_200_OK
                )
            except EmploymentRecord.DoesNotExist:
                return response.Response(
                    data={"employment_record": "Does Not Exist"},
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


class SkillsView(generics.GenericAPIView):
    """
    A generic API view for handling skills.

    Attributes:
        - `permission_classes (list)`: The list of permission classes that the user must have to access this view.
                                In this case, only authenticated users can access this view.

        - `serializer_class (JobSeekerSkillSerializers)`: The serializer class that the view uses to serialize and
                                                deserialize the JobSeekerSkill model.

    Returns:
        Serialized skills in JSON format, with authentication required to access the view. 
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = JobSeekerSkillSerializers

    def post(self, request):
        """
        Handles HTTP POST requests for creating a new skills.

        Args:
            request (HttpRequest): The request object sent to the server.

        Returns:
            HTTP response with serialized data in JSON format, and status codes indicating whether the request was
            successful or not.

        Raises:
            serializers.ValidationError: If the data in the request is invalid or incomplete.

            Exception: If an error occurs while processing the request.

        Notes:
            This function creates a new skills using the serializer class specified in the `serializer_class`
            attribute of the view. The serializer is first validated and then saved to the database. The `user` field
            of the skills is set to the currently logged-in user.
            If the serializer is not valid, a `serializers.ValidationError` is raised and a response with a status code
            of 400 is returned. If any other error occurs, a response with a status code of 400 is returned along with
            an error message in the `message` field of the response data. If the serializer is valid and the record is
            successfully created, a response with the serialized data and a status code of 201 is returned.
        """

        context = dict()
        if request.user.role == "job_seeker":
            serializer = self.serializer_class(data=request.data)
            try:
                serializer.is_valid(raise_exception=True)
                for data in serializer.validated_data:
                    try:
                        if JobSeekerSkill.objects.get(skill_id=data, user=request.user):
                            pass
                    except JobSeekerSkill.DoesNotExist:
                        JobSeekerSkill.objects.create(skill_id=data, user=request.user)
                context["message"] = "Skills added."
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
        else:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
            )


class JobsApplyView(generics.GenericAPIView):
    """View for creating a new job application.

    This view handles the creation of a new job application by authenticating the user making the request and then
    using the AppliedJobSerializers to deserialize the request data and save the new job application.

    Attributes:
        - permission_classes (list): A list of permission classes that a user must have in order to access this view.
        - serializer_class (AppliedJobSerializers): The serializer class that will be used to deserialize the incoming
            data and serialize the outgoing data.

    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AppliedJobSerializers

    def post(self, request, jobId):
        """
        Creates a new application for a job posting by a job seeker.

        Args:
            request: The HTTP request object.
            jobId (int): The ID of the job posting to apply for.

        Returns:
            A response object with the following keys:
            - "message" (str): A message indicating the success or failure of the request.

            - If the request is successful, the response will have a status code of 200 (HTTP_200_OK).
            - If the user does not have permission to perform this action, the response will have a status
            code of 401 (HTTP_401_UNAUTHORIZED).
            - If the specified job posting does not exist, the response will have a status code of 404
            (HTTP_404_NOT_FOUND).
            - If there is an error while processing the request, the response will have a status code of 404
            (HTTP_404_NOT_FOUND) and a message describing the error.
        """

        context = dict()
        if request.user.role == "job_seeker":
            try:
                job_instace = JobDetails.objects.get(id=jobId)
                try:
                    if AppliedJob.objects.get(job=job_instace, user=request.user):
                        context["message"] = "You are already applied"
                        return response.Response(
                            data=context,
                            status=status.HTTP_400_BAD_REQUEST
                        )
                except AppliedJob.DoesNotExist:
                    serializer = self.serializer_class(data=request.data)
                    try:
                        serializer.is_valid(raise_exception=True)
                        serializer.save(user=request.user, job_instace=job_instace)
                        context["message"] = "Applied Successfully"
                        return response.Response(
                            data=context,
                            status=status.HTTP_200_OK
                        )
                    except serializers.ValidationError:
                        return response.Response(
                            data=str(serializer.errors),
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

        else:
            context['message'] = "You do not have permission to perform this action."
            return response.Response(
                data=context,
                status=status.HTTP_401_UNAUTHORIZED
            )
