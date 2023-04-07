from django.shortcuts import get_object_or_404

from rest_framework import (
    generics, response, status,
    permissions, serializers, filters
)

from core.pagination import CustomPagination

from user_profile.models import VendorProfile

from tenders.models import TenderDetails

from .models import SavedTender
from .serializers import (
    UpdateAboutSerializers,
    SavedTenderSerializers,
    GetSavedTenderSerializers

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
        if 'search_by' in self.request.GET:
            search_by = self.request.GET['search_by']
            if search_by == 'salary':
                order_by = 'tender__budget_amount'
            elif search_by == 'expiration':
                order_by = 'tender__deadline'
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
