from django.shortcuts import get_object_or_404

from rest_framework import (
    generics, response, status,
    permissions, serializers
)

from tenders.models import TenderDetails

from user_profile.models import VendorProfile

from .models import SavedTender
from .serializers import (
    UpdateAboutSerializers,
    SavedTenderSerializers

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
    A view that lists all saved tenders for the authenticated user.

    Attributes:
        - `permission_classes (list)`: a list of permission classes that the user must have in order to access this
            view.
            In this case, only authenticated users can access this view.

    Methods:
        - `get(self, request, *args, **kwargs)`: retrieves the saved tenders for the authenticated user.
            - `Args`:
                - `request (HttpRequest)`: the HTTP request object that contains the request data.
                - `*args`: variable length argument list.
               - ` **kwargs`: keyword arguments.
            - `Returns:
                - A serialized list of saved tenders for the authenticated user.
    """

    permission_classes = [permissions.IsAuthenticated]

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
