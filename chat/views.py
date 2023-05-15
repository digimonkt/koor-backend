# chat/views.py
from django.shortcuts import redirect
from django.views.generic import View, DetailView
from rest_framework import generics, renderers, authentication, response
from rest_framework_simplejwt.authentication import JWTAuthentication

# from core.models import Media
# from core.serializers import MediaSerializer
from core.pagination import CustomPagination
from .models import ChatMessage, Conversation
from .paginations import LinkPagination
from .serializers import ChatMessageSerializer, ConversationSerializer


class ChatView(View):
    template_name = 'chat/base.html'

    def get(self, request, *args, **kwargs):
        print(request)
        # conversation = request.user.conversation_participants.last()
        # return redirect('chat:chat_room', room_name="str(conversation.id)")
        return redirect('chat:chat_room', room_name=str("e9dfd38e-d61d-4b8e-93c9-0c197e2b17ee"))


class ConversationListView(generics.ListAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    pagination_class = LinkPagination
    renderer_classes = [renderers.JSONRenderer, ]
    authentication_classes = [authentication.SessionAuthentication, JWTAuthentication]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(filtered_queryset, many=True)
        return response.Response(serializer.data)


class ChatRoomView(DetailView):
    model = Conversation
    queryset = Conversation.objects.all()
    context_object_name = "conversation"
    template_name = "chat/room.html"
    lookup_field = 'room_name'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        queryset = queryset.filter(id=self.kwargs['room_name'])
        print(queryset, "queryset_value")
        obj = queryset.get()
        return obj


class ChatHistory(generics.ListAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    pagination_class = CustomPagination
    renderer_classes = [renderers.JSONRenderer, ]
    authentication_classes = [authentication.SessionAuthentication, JWTAuthentication]

    def list(self, request, agent_id):
        conversation = Conversation.objects.get(id=agent_id)
        queryset = self.filter_queryset(self.get_queryset().filter(conversation=conversation))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

        # qs = self.get_queryset()
        # try:
        #     conversation = Conversation.objects.get(id=agent_id)
        #     chat_messages = qs.filter(conversation=conversation)
        #     print(chat_messages, "messages")
        #     # conversation.mark_messages_as_read(request.user)

        # except Conversation.DoesNotExist:
        #     chat_messages = ChatMessage.objects.none()
        # # Initialize pagination object with request
        # paginator = self.pagination_class()
        # paginated_messages = paginator.paginate_queryset(chat_messages, request)

        # data = self.serializer_class(paginated_messages, many=True).data
        # return paginator.get_paginated_response(data)
