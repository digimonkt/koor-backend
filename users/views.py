from rest_framework import (
    status, generics, serializers,
    response, permissions
)
from core.tokens import SessionTokenObtainPairSerializer

from .models import UserSession, User
from .serializers import (
    CreateUserSerializers,
    CreateSessionSerializers
    )

def create_user_session(request, user):
        """
        `create_user_session` creates a new UserSession object for the given request. It retrieves the IP address from the request and stores the user agent in the agent field.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            IPAddr = x_forwarded_for.split(',')[0]
        else:
            IPAddr = request.META.get('REMOTE_ADDR')
        agent = {'User-Agent': request.headers.get('User-Agent')}
        user_session = UserSession.objects.create(
            user=user, 
            ip_address=IPAddr, 
            agent=agent
        )
        user_session.save()
        return user_session

class CreateUserView(generics.CreateAPIView):
    serializer_class = CreateUserSerializers
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        context = dict()  
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user = User.objects.get(id=serializer.data['id'])
            user.set_password(serializer.data['password'])
            user.save()
            user_session = create_user_session(request, user,)

            token = SessionTokenObtainPairSerializer.get_token(
                user=user,
                session_id=user_session.id
            )
            context["message"] = "User Created Successfully"
            return response.Response(
                data=context,
                headers={"x-access": token.access_token, "x-refresh": token},
                status=status.HTTP_201_CREATED
            )
        except serializers.ValidationError:
            return response.Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class CreateSessionView(generics.CreateAPIView):
    """
    CreateAPIView for creating a session for a user.

    Uses the CreateSessionSerializers serializer class to validate and
    handle user data. 

    Attributes:
        serializer_class (CreateSessionSerializers): The serializer class to use.
        permission_classes ([permissions.AllowAny]): The permission classes.

    Methods:
        post(request): Handles the POST request to create a user session.
    """

    serializer_class = CreateSessionSerializers
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        context = dict()  
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user_session = create_user_session(request, serializer.validated_data)
            token = SessionTokenObtainPairSerializer.get_token(
                user=serializer.validated_data,
                session_id=user_session.id
            )
            context["message"] = "User LoggedIn Successfully"
            return response.Response(
                data=context,
                headers={"x-access": token.access_token, "x-refresh": token},
                status=status.HTTP_201_CREATED
            )
        except serializers.ValidationError:
            return response.Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
