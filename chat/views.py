from django.db.models import Q
from rest_framework import (
    status, generics, serializers,
    response, permissions
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
        queryset = self.filter_queryset(self.get_queryset(request, conversationId))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def get_queryset(self, request, conversationId, **kwargs):
        conversation = Conversation.objects.get(id=conversationId)
        message_id = self.request.GET.get('messageId', None)
        if not message_id:
            return ChatMessage.objects.filter(conversation=conversation).order_by('-created')
        current_object = ChatMessage.objects.get(id=message_id)
        return ChatMessage.objects.filter(conversation=conversation).filter(created__lt=current_object.created).order_by('-created')


class Attachment(generics.GenericAPIView):
    serializer_class = UploadAttachmentSerializers
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        context = dict()
        response_context = dict()
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            get_url = serializer.save()
            return response.Response(
                data=get_url,
                status=status.HTTP_201_CREATED
            )
        except serializers.ValidationError:
            return response.Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
