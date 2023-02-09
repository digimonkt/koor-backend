from rest_framework import (
    status, generics, serializers,
    response, permissions
)

from .serializers import (
    CreateCountrySerializers
)


class CountryView(generics.GenericAPIView):
    """
    API View class for creating a new country.

    The `CountryView` class extends the `generics.GenericAPIView` and is used to create a new country in the system.
    The `post` method is overridden to handle the creation of the country. The serializer class used for this view is
    `CreateCountrySerializers`. The view requires authentication and only allows users with the role "admin" and staff
    status to create a new country.

    - If the request is successful, a 201 CREATED response is returned with a message indicating that the country was
      added successfully.

    - If the user does not have the required permissions, a 401 UNAUTHORIZED response is returned with a message
      indicating that the user does not have permission to perform the action.

    - If the serializer raises a validation error, a 400 BAD REQUEST response is returned with the error messages.

    - If an exception is raised, a 400 BAD REQUEST response is returned with the exception message as a string.
    
    """
    
    serializer_class = CreateCountrySerializers
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
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
            return response.Response(
                data=str(e),
                status=status.HTTP_400_BAD_REQUEST
            )
