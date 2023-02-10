from rest_framework import (
    status, generics, serializers,
    response, permissions
)

from .serializers import (
    CreateCountrySerializers
)


class CountryView(generics.GenericAPIView):
    """
    A generic API view for creating and retrieving countries.

    This class is based on the Django REST framework's `generics.GenericAPIView` class and is used to handle the creation
    and retrieval of country objects. It enforces authentication using the `permissions.IsAuthenticated` permission class
    and uses the `CreateCountrySerializers` serializer class to validate and serialize data.
    """
    
    serializer_class = CreateCountrySerializers
    permission_classes = [permissions.IsAuthenticated]

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
