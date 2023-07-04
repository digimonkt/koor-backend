from django.db.models import Q
from rest_framework import (
    status, generics, serializers,
    response, permissions, filters
)

from core.pagination import CustomPagination
from users.models import User

from .models import ChatMessage, Conversation
from .serializers import (
    ChatMessageSerializer, ConversationSerializer,
    UploadAttachmentSerializers
)


class ConversationListView(generics.ListAPIView):
    """
    API view for listing conversations.

    This view returns a paginated list of conversations filtered by the current user, excluding conversations with no
    last message. The conversations are serialized using the ConversationSerializer class.

    Required permissions:
        - AllowAny: All users have access to this view.

    Pagination:
        - The paginated response is based on the CustomPagination class.

    HTTP Methods:
        - GET: Retrieves the paginated list of conversations.

    Query Parameters:
        - None

    Response:
        - If pagination is applied and there are paginated results, the response includes the paginated data with
            pagination metadata.
        - If pagination is not applied or there are no paginated results, the response includes the serialized data
        for all conversations.
    """

    serializer_class = ConversationSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Conversation.objects.all()
    pagination_class = CustomPagination

    def list(self, request):
        search_query = request.GET.get('search', None)
        if search_query:
            chat_user1 = []
            logged_in_user = request.user  # Replace with your logged-in user retrieval logic

            # Retrieve conversations that have chat users matching the search query
            conversations = Conversation.objects.filter(chat_user__name__icontains=search_query)

            # Get all chat users from the conversations
            chat_users = conversations.values_list('chat_user', flat=True).distinct()
            for chat in chat_users:
                if chat != self.request.user.id:
                    chat_user1.append(chat)
            filtered_queryset = self.filter_queryset(
                self.get_queryset().filter(chat_user=self.request.user).filter(chat_user__id__in=chat_user1).filter(~Q(last_message=None))
            )
        else:
            filtered_queryset = self.filter_queryset(
                self.get_queryset().filter(chat_user=self.request.user).filter(~Q(last_message=None))
            )
        paginated_queryset = self.paginate_queryset(filtered_queryset)

        serializer = self.get_serializer(
            paginated_queryset or filtered_queryset,
            many=True,
            context={'user': self.request.user}
        )
        return self.get_paginated_response(serializer.data) if paginated_queryset else response.Response(
            serializer.data
        )


class GetConversationView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, userId):
        """
        Get the conversation ID between the authenticated user and the specified user ID.

        Args:
            request (HttpRequest): The HTTP request object.
            userId (int): The ID of the user to retrieve the conversation for.

        Returns:
            A response object with the following possible statuses:
            - 200 OK: If the conversation exists, returns the conversation ID in the response data.
            - 404 NOT FOUND: If the specified user ID does not exist.
            - 400 BAD REQUEST: If an error occurred during the conversation retrieval.

        Raises:
            N/A
        """
        
        context = {}

        try:
            user_instance = User.objects.get(id=userId)
            conversation = Conversation.objects.get(chat_user=self.request.user and user_instance)
            context['conversation_id'] = conversation.id
            return response.Response(data=context, status=status.HTTP_200_OK)

        except Conversation.DoesNotExist:
            return response.Response(data=context, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return response.Response(data={'userId': 'Invalid userId'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            context["error"] = str(e)
            return response.Response(data=context, status=status.HTTP_400_BAD_REQUEST)


class ChatHistory(generics.ListAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.AllowAny]
    queryset = None
    pagination_class = CustomPagination

    def list(self, request, conversationId):
        """
        Retrieve a paginated list of chat messages for a given conversation ID.

        Args:
            request (HttpRequest): The HTTP request object.
            conversationId (int): The ID of the conversation to retrieve messages for.

        Returns:
            Response: A paginated response containing serialized chat messages.
        """

        queryset = self.get_queryset(request, conversationId)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True) if page is not None else self.get_serializer(queryset, many=True)
        return self.get_paginated_response(serializer.data) if page is not None else response.Response(serializer.data)

    def get_queryset(self, request, conversationId, **kwargs):
        """
        Retrieve the queryset of chat messages for a given conversation ID.

        Args:
            request (HttpRequest): The HTTP request object.
            conversationId (int): The ID of the conversation to retrieve messages for.
            kwargs (dict): Additional keyword arguments.

        Returns:
            QuerySet: The queryset of chat messages.
        """

        conversation = Conversation.objects.get(id=conversationId)
        message_id = self.request.GET.get('messageId')
        if message_id:
            current_object = ChatMessage.objects.get(id=message_id)
            return ChatMessage.objects.filter(conversation=conversation, created__lt=current_object.created).order_by('-created')
        return ChatMessage.objects.filter(conversation=conversation).order_by('-created')


class Attachment(generics.GenericAPIView):
    """
    A view for uploading attachments.

    This class-based view handles the HTTP POST request for uploading attachments.
        - It uses the specified serializer to validate the request data and save the attachment.
        - If the data is valid, the view returns the URL of the saved attachment with a status code of 201.
        - If there are validation errors, the view returns the error details with a status code of 400.

    Attributes:
        - serializer_class (Serializer): The serializer class used to validate and save the attachment.
        - permission_classes (list): A list of permission classes applied to the view.

    Methods:
        - post(request): Handles the POST request for uploading attachments.

    Raises:
        - serializers.ValidationError: If the provided data is invalid according to the serializer.

    Returns:
        - A Response object containing the result of the upload operation.

    """

    serializer_class = UploadAttachmentSerializers
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Handles the HTTP POST request for uploading attachments.

        Parameters:
            request (HttpRequest): The request object containing the attachment data.

        Returns:
            A Response object containing the result of the upload operation.
        """

        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            get_url = serializer.save()
            return response.Response(data=get_url, status=status.HTTP_201_CREATED)
        except serializers.ValidationError:
            return response.Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
