from django.shortcuts import get_object_or_404
from datetime import date

from rest_framework import (
    generics, response, status,
    permissions, serializers, filters
)

from core.pagination import CustomPagination

from user_profile.models import VendorProfile

from tenders.models import TenderDetails

from .models import (
    SavedTender, AppliedTender, VendorSector,
    VendorTag
)
from .serializers import (
    UpdateAboutSerializers, SavedTenderSerializers,
    GetSavedTenderSerializers, GetAppliedTenderSerializers,
    AppliedTenderSerializers, UpdateAppliedTenderSerializers,
    VendorSectorSerializers, VendorTagSerializers
)


class UpdateAboutView(generics.GenericAPIView):
    """
    A view for updating the VendorProfile of the currently authenticated User.

    Attributes:
        serializer_class: The serializer class to use for updating the VendorProfile.
        permission_classes: The permission classes required to access this view.

    Methods:
        patch: Handle PATCH requests to update the VendorProfile of the authenticated User.

    Returns:
        A Response object with a success or error message, and an appropriate status code.
    """

    serializer_class = UpdateAboutSerializers
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        context = dict()
        if self.request.user.role == "vendor":
            profile_instance = get_object_or_404(VendorProfile, user=request.user)
            serializer = self.serializer_class(data=request.data, instance=profile_instance, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                if 'email' in serializer.validated_data:
                    if User.objects.filter(email__iexact=serializer.validated_data['email']).exists():
                        if profile_instance.user.email__iexact != serializer.validated_data['email']:
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


class TenderSaveView(generics.ListAPIView):
    """
    View for retrieving saved tenders by authenticated users.

    - `serializer_class`: A serializer class for `serializing/deserializing` the saved tender data.
    - `permission_classes`: A list of permission classes that define the permission policy for this view.
    - `queryset`: The queryset used for retrieving the saved tenders. This is set to None as the actual queryset is
        generated dynamically based on the authenticated user.
    - `filter_backends`: A list of filter backend classes used for filtering the saved tenders.
    - `search_fields`: A list of fields on which the search filter should be applied.
    - `pagination_class`: A pagination class used for pagination of the retrieved saved tenders.

    """

    serializer_class = GetSavedTenderSerializers
    permission_classes = [permissions.IsAuthenticated]
    queryset = None
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    pagination_class = CustomPagination

    def list(self, request):
        """
        Returns a paginated list of serialized saved tenders for the authenticated user.

        This method returns a paginated list of saved tenders for the authenticated user. The saved tenders are
        serialized using the `GetSavedTenderSerializers` class.

        Args:
            request: The HTTP request object.

        Returns:
            A HTTP response object containing a paginated list of serialized saved tenders.

        The response includes the following fields:
            - `count (int)`: The total number of saved tenders for the authenticated user.
            - `next (str)`: The URL for the next page of results, or null if there are no more pages.
            - `previous (str)`: The URL for the previous page of results, or null if this is the first page.
            - `results (list)`: A list of serialized saved tenders for the authenticated user.

        """

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, context={"request": request})
        return response.Response(serializer.data)

    def get_queryset(self, **kwargs):
        """
        Returns the queryset of saved tenders for the authenticated user.

        This method returns a queryset of SavedTender objects for the authenticated user, ordered by their creation date
        in descending order.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            A queryset of SavedTender objects for the authenticated user, ordered by their creation date in descending
            order.
        """
        order_by = None
        if 'search_by' in self.request.GET:
            search_by = self.request.GET['search_by']
            if search_by == 'salary':
                order_by = 'tender__budget_amount'
            elif search_by == 'expiration':
                order_by = 'tender__deadline'
            elif search_by == 'created_at':
                order_by = 'tender__created'
            if order_by:
                if 'order_by' in self.request.GET:
                    if 'descending' in self.request.GET['order_by']:
                        return SavedTender.objects.filter(
                            user=self.request.user,
                            tender__is_removed=False
                        ).order_by("-" + str(order_by))
                    else:
                        return SavedTender.objects.filter(
                            user=self.request.user,
                            ob__is_removed=False
                        ).order_by(str(order_by))
                else:
                    return SavedTender.objects.filter(
                        user=self.request.user,
                        tender__is_removed=False
                    ).order_by(str(order_by))
        return SavedTender.objects.filter(
            user=self.request.user,
            tender__is_removed=False
        )

    def post(self, request, tenderId):
        """
        A view that saves a tender for a vendor user.

        Methods:
            - `post`(self, request, tenderId): creates a `SavedTender` instance for the specified tender and user.
                - `Args`:
                    - `request` (HttpRequest): the HTTP request object that contains the request data.
                    - `tenderId` (int): the ID of the tender instance to be saved.
                - Returns:
                    - A response object with data about the `success or failure` of the save operation.
                    - If `successful`, the response data will include a "message" field with the value
                        "`Saved Successfully`".
                    - If the user has `already saved` the tender, the response data will include a "message" field with
                        the value "`You are already saved`" and a status code of `400`.
                    - If the tender with the specified `ID does not exist`, the response data will include a "tender"
                        field with the value "`Does Not Exist`" and a status code of `404`.
                    - If the user is `not a vendor`, the response data will include a "message" field with the value
                        "`You do not have permission to perform this action`" and a status code of `401`.
                    - If there is a `validation error` with the serializer, the response data will include a string
                        representation of the `error messages` and a status code of `400`.
        """

        context = dict()
        if request.user.role == "vendor":
            try:
                tender_instace = TenderDetails.objects.get(id=tenderId)
                try:
                    if SavedTender.objects.get(tender=tender_instace, user=request.user):
                        context["message"] = "You are already saved"
                        return response.Response(
                            data=context,
                            status=status.HTTP_400_BAD_REQUEST
                        )
                except SavedTender.DoesNotExist:
                    serializer = SavedTenderSerializers(data=request.data)
                    try:
                        serializer.is_valid(raise_exception=True)
                        serializer.save(user=request.user, tender_instace=tender_instace)
                        context["message"] = "Saved Successfully"
                        return response.Response(
                            data=context,
                            status=status.HTTP_200_OK
                        )
                    except serializers.ValidationError:
                        return response.Response(
                            data=str(serializer.errors),
                            status=status.HTTP_400_BAD_REQUEST
                        )
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

    def delete(self, request, tenderId):
        """
        Deletes an SavedTender object with the given tender if the authenticated user is a vendor and owns the
        SavedTender.
        Args:
            request: A DRF request object.
            tenderId: An integer representing the ID of the SavedTender to be deleted.
        Returns:
            A DRF response object with a success or error message and appropriate status code.
        """
        context = dict()
        if request.user.role == "vendor":
            try:
                tender_instace = TenderDetails.objects.get(id=tenderId)
                try:
                    SavedTender.all_objects.get(tender=tender_instace, user=request.user).delete(soft=False)
                    context['message'] = "Tender Unsaved"
                    return response.Response(
                        data=context,
                        status=status.HTTP_200_OK
                    )
                except SavedTender.DoesNotExist:
                    return response.Response(
                        data={"savedTenderId": "Does Not Exist"},
                        status=status.HTTP_404_NOT_FOUND
                    )
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


class TenderApplyView(generics.ListAPIView):
    """
    A view for retrieving a list of applied tender.

    This view supports HTTP GET requests and returns a list of applied tender for the authenticated user.
    The applied tender are serialized using the `GetAppliedTenderSerializers` class.

    This view requires the user to be authenticated, and uses the `IsAuthenticated` permission class.
    The view supports searching the applied tender by job title, using the `SearchFilter` filter backend.

    Attributes:
        - `serializer_class`: The serializer class to use for serializing the applied tender.
        - `permission_classes`: A list of permission classes that the user must pass in order to access this view.
        - `queryset`: The base queryset for the view. This attribute is not used in this view, since the queryset
            is dynamically generated in the `get_queryset` method.
        - `filter_backends`: A list of filter backends to use for filtering the applied tender.
        - `search_fields`: The fields to search for when filtering the applied tender.
    """

    serializer_class = GetAppliedTenderSerializers
    permission_classes = [permissions.IsAuthenticated]
    queryset = None
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    pagination_class = CustomPagination

    def list(self, request):
        """
        Returns a paginated list of serialized applied tender for the authenticated user.

        This method returns a paginated list of applied tender for the authenticated user. The applied tender are
        serialized using the `GetAppliedTenderSerializers` class.

        Args:
            request: The HTTP request object.

        Returns:
            A HTTP response object containing a paginated list of serialized applied tender.

        The response includes the following fields:
            - `count (int)`: The total number of applied tender for the authenticated user.
            - `next (str)`: The URL for the next page of results, or null if there are no more pages.
            - `previous (str)`: The URL for the previous page of results, or null if this is the first page.
            - `results (list)`: A list of serialized applied tender for the authenticated user.

        """

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, context={"request": request})
        return response.Response(serializer.data)

    def post(self, request, tenderId):
        """
        Creates a new application for a tender posting by a vendor.

        Args:
            request: The HTTP request object.
            tenderId (int): The ID of the tender posting to apply for.

        Returns:
            A response object with the following keys:
            - "message" (str): A message indicating the success or failure of the request.

            - If the request is successful, the response will have a status code of 200 (HTTP_200_OK).
            - If the user does not have permission to perform this action, the response will have a status
            code of 401 (HTTP_401_UNAUTHORIZED).
            - If the specified tender posting does not exist, the response will have a status code of 404
            (HTTP_404_NOT_FOUND).
            - If there is an error while processing the request, the response will have a status code of 404
            (HTTP_404_NOT_FOUND) and a message describing the error.
        """

        context = dict()
        if request.user.role == "vendor":
            try:
                tender_instace = TenderDetails.objects.get(id=tenderId)
                try:
                    if AppliedTender.objects.get(tender=tender_instace, user=request.user):
                        context["message"] = "You are already applied"
                        return response.Response(
                            data=context,
                            status=status.HTTP_400_BAD_REQUEST
                        )
                except AppliedTender.DoesNotExist:
                    serializer = AppliedTenderSerializers(data=request.data)
                    try:
                        serializer.is_valid(raise_exception=True)
                        serializer.save(user=request.user, tender_instace=tender_instace)
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

    def put(self, request, tenderId):
        """
        Update an existing tender application for a vendor user.

        Args:
            - `request`: An HTTP request object.
            - `tenderId (int)`: The ID of the tender application to update.

        Returns:
            A Response object with an appropriate HTTP status code and message.

        Raises:
            - `ValidationError`: If the request data is invalid.
            - `Http404`: If the specified tender or tender application does not exist.
            - `Exception`: If any other error occurs.

        The function first checks if the user making the request is a vendor. If not, it returns an
        unauthorized response. Otherwise, it tries to update the specified tender application with the given
        data using an instance of the UpdateTenderSerializers class. If the update is successful, it returns
        a success response with a message indicating that the update was successful. If the tender application
        or tender do not exist, it returns a 404 response with an appropriate error message. If the request data
        is invalid or if any other error occurs, it returns a 400 or 404 response with an error message
        containing details about the error.
        """

        context = dict()
        if self.request.user.role == "vendor":
            serializer = UpdateAppliedTenderSerializers(data=request.data)
            try:
                tender_instace = TenderDetails.objects.get(id=tenderId)
                try:
                    applied_tender = AppliedTender.objects.get(tender=tender_instace, user=request.user)
                    if applied_tender.shortlisted_at or applied_tender.rejected_at or applied_tender.created.date() < date.today():
                        context['message'] = "You cannot update this applied tender"
                        return response.Response(
                            data=context,
                            status=status.HTTP_200_OK
                        )
                    else:
                        serializer.is_valid(raise_exception=True)
                        if serializer.update(applied_tender, serializer.validated_data):
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
                except AppliedTender.DoesNotExist:
                    return response.Response(
                        data={"application": "Does Not Exist"},
                        status=status.HTTP_404_NOT_FOUND
                    )
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

    def delete(self, request, tenderId):
        """
        Deletes an AppliedTender object with the given tender if the authenticated user is a vendor and owns the
        AppliedTender.
        Args:
            request: A DRF request object.
            educationId: An integer representing the ID of the AppliedTender to be deleted.
        Returns:
            A DRF response object with a success or error message and appropriate status code.
        """
        context = dict()
        if request.user.role == "vendor":
            try:
                tender_instace = TenderDetails.objects.get(id=tenderId)
                try:
                    applied_tender = AppliedTender.objects.get(tender=tender_instace, user=request.user)
                    if applied_tender.shortlisted_at or applied_tender.rejected_at or applied_tender.created.date() < date.today():
                        context['message'] = "You cannot revoke this applied tender"
                    else:
                        applied_tender.delete()
                        context['message'] = "Revoked applied tender"
                    return response.Response(
                        data=context,
                        status=status.HTTP_200_OK
                    )
                except AppliedTender.DoesNotExist:
                    return response.Response(
                        data={"AppliedTender": "Does Not Exist"},
                        status=status.HTTP_404_NOT_FOUND
                    )
                except Exception as e:
                    context["message"] = e
                    return response.Response(
                        data=context,
                        status=status.HTTP_404_NOT_FOUND
                    )
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

    def get_queryset(self, **kwargs):
        """
        Returns the queryset of applied tender for the authenticated user.

        This method returns a queryset of AppliedTender objects for the authenticated user, ordered by their creation date
        in descending order.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            A queryset of AppliedTender objects for the authenticated user, ordered by their creation date in descending
            order.
        """
        order_by = None
        if 'search_by' in self.request.GET:
            search_by = self.request.GET['search_by']
            if search_by == 'salary':
                order_by = 'tender__budget_amount'
            elif search_by == 'expiration':
                order_by = 'tender__deadline'
            elif search_by == 'created_at':
                order_by = 'tender__created'
            if order_by:
                if 'order_by' in self.request.GET:
                    if 'descending' in self.request.GET['order_by']:
                        return AppliedTender.objects.filter(
                            user=self.request.user,
                            tender__is_removed=False
                        ).order_by("-" + str(order_by))
                    else:
                        return AppliedTender.objects.filter(
                            user=self.request.user,
                            tender__is_removed=False
                        ).order_by(str(order_by))
                else:
                    return AppliedTender.objects.filter(
                        user=self.request.user,
                        tender__is_removed=False
                    ).order_by(str(order_by))
        return AppliedTender.objects.filter(
            user=self.request.user,
            tender__is_removed=False
        )


class SectorView(generics.GenericAPIView):
    """
    A class-based view for handling vendor sectors.

    This class extends the `generics.GenericAPIView` class and provides functionality for managing vendor sectors.
    It requires authentication for accessing its endpoints and uses the `VendorSectorSerializers` serializer class.

    Attributes:
        permission_classes (list): A list of permission classes applied to this view. Requires authentication.
        serializer_class (class): The serializer class used for validating and deserializing input data.

    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VendorSectorSerializers

    def post(self, request):
        """
        Handles the POST request to add sectors for a vendor.

        Parameters:
        - request (HttpRequest): The HTTP request object containing the user and data.

        Returns:
        - Response: The API response indicating the success or failure of the sector addition.

        Raises:
        - ValidationError: If the data in the request is not valid.

        Description:
        - This function is used to add sectors for a vendor. It expects the user to have the "vendor" role.
        - It validates the data received in the request against the serializer class.
        - If the data is valid, it checks if the vendor already has a sector with the given sector_id.
        - If not, it creates a new VendorSector object for each sector_id and associates it with the vendor.
        - Finally, it returns a response indicating the success or failure of the sector addition.
        - If the user does not have the "vendor" role, an unauthorized response is returned.
        """

        context = dict()
        if request.user.role == "vendor":
            serializer = self.serializer_class(data=request.data)
            try:
                serializer.is_valid(raise_exception=True)
                for data in serializer.validated_data:
                    try:
                        if VendorSector.objects.get(sector_id=data, user=request.user):
                            pass
                    except VendorSector.DoesNotExist:
                        VendorSector.objects.create(sector_id=data, user=request.user)
                context["message"] = "Sector added."
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


class TagView(generics.GenericAPIView):
    """
    A class-based view for handling vendor tags.

    This class extends the `generics.GenericAPIView` class and provides functionality for managing vendor tags.
    It requires authentication for accessing its endpoints and uses the `VendorTagSerializers` serializer class.

    Attributes:
        permission_classes (list): A list of permission classes applied to this view. Requires authentication.
        serializer_class (class): The serializer class used for validating and deserializing input data.

    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VendorTagSerializers

    def post(self, request):
        """
        Handles the POST request to add tags for a vendor.

        Parameters:
        - request (HttpRequest): The HTTP request object containing the user and data.

        Returns:
        - Response: The API response indicating the success or failure of the tag addition.

        Raises:
        - ValidationError: If the data in the request is not valid.

        Description:
        - This function is used to add tags for a vendor. It expects the user to have the "vendor" role.
        - It validates the data received in the request against the serializer class.
        - If the data is valid, it checks if the vendor already has a tag with the given tag_id.
        - If not, it creates a new VendorTag object for each tag_id and associates it with the vendor.
        - Finally, it returns a response indicating the success or failure of the tag addition.
        - If the user does not have the "vendor" role, an unauthorized response is returned.
        """

        context = dict()
        if request.user.role == "vendor":
            serializer = self.serializer_class(data=request.data)
            try:
                serializer.is_valid(raise_exception=True)
                for data in serializer.validated_data:
                    try:
                        if VendorTag.objects.get(tag_id=data, user=request.user):
                            pass
                    except VendorTag.DoesNotExist:
                        VendorTag.objects.create(tag_id=data, user=request.user)
                context["message"] = "Tag added."
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


class TenderApplyByEmailView(generics.GenericAPIView):
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, tenderId):
        
        context = dict()
        blacklisted_user = []
        if request.user.role == "vendor":
            try:
                tender_instance = TenderDetails.objects.get(id=tenderId)
                blacklisted_list = BlackList.objects.filter(user=tender_instance.user)
                for blacklisted_data in blacklisted_list:
                    blacklisted_user.append(blacklisted_data.blacklisted_user)
                if request.user in blacklisted_user:
                    context["message"] = ["You are blacklisted for this Tender."]
                    return response.Response(
                        data=context,
                        status=status.HTTP_400_BAD_REQUEST
                    )
                try:
                    if AppliedTender.objects.get(tender=tender_instance, user=request.user):
                        context["message"] = ["You are already applied"]
                        return response.Response(
                            data=context,
                            status=status.HTTP_400_BAD_REQUEST
                        )
                except AppliedTender.DoesNotExist:
                    if tender_instance.apply_through_email:
                        user_email = []
                        if tender_instance.user:
                            if tender_instance.user.email:
                                user_email.append(tender_instance.user.email)
                        if tender_instance.contact_email:
                            user_email.append(tender_instance.contact_email)
                        if tender_instance.cc1:
                            user_email.append(tender_instance.cc1)
                        if tender_instance.cc2:
                            user_email.append(tender_instance.cc2)
                        if user_email:
                            email_context = dict()
                            if tender_instance.user:
                                if tender_instance.user.name:
                                    user_name = tender_instance.user.name
                                else:
                                    user_name = user_email[0]
                            elif tender_instance.company:
                                user_name = tender_instance.company
                            else:
                                user_name = user_email[0]
                            email_context["yourname"] = user_name
                            email_context["username"] = request.user
                            email_context["resume_link"] = Common.BASE_URL
                            email_context["notification_type"] = "applied tender"
                            email_context["tender_instance"] = tender_instance
                            get_email_object(
                                subject=f'Applied tender through email',
                                email_template_name='email-templates/mail-for-apply-tender.html',
                                context=email_context,
                                to_email=user_email
                            )
                            context["message"] = ["Applied Successfully"]
                            return response.Response(
                                data=context,
                                status=status.HTTP_200_OK
                            )
                        else:
                            context["message"] = ["Employer email not detected."]
                            return response.Response(
                                data=context,
                                status=status.HTTP_400_BAD_REQUEST
                            )
                        
                    else:
                        context["message"] = ["Employer not active apply through email."]
                        return response.Response(
                            data=context,
                            status=status.HTTP_400_BAD_REQUEST
                        )
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
