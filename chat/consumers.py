import logging
from django.db.models import Q
import jwt
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from koor.config.common import Common
from users.models import UserSession, User
from project_meta.models import Media
from .models import Conversation, ChatMessage
from .serializers import ChatMessageSerializer, ConversationSerializer

# Get JWT secret key
SECRET_KEY = settings.SECRET_KEY

class BaseConsumer(JsonWebsocketConsumer):
    """
    Base consumer class for handling websocket connections.
    """

    def get_session(self, session_id, uid):
        """
        Get the user session for the given session ID.
        
        Args:
            session_id (str): ID of the user session.
            uid (str): ID of the user.
        
        Returns:
            UserSession or None: UserSession object if found, None otherwise.
        """
        try:
            session = UserSession.objects.get(id=session_id, user_id=uid)
            return session
        except UserSession.DoesNotExist:
            return None

    def authenticate(self):
        """
        Authenticate the websocket connection and set the authenticated user in the scope.
        """
        logger = logging.getLogger(__name__)
        try:
            session_id = None
            uid = None
            chat_url = self.scope['query_string'].decode()
            if 'sid=' in chat_url:
                session_id = chat_url.split('sid=')[1].split('&')[0]
            elif '&sid=' in chat_url:
                session_id = chat_url.split('&sid=')[1].split('&')[0]
            if 'uid=' in chat_url:
                uid = chat_url.split('uid=')[1].split('&')[0]
            elif '&uid=' in chat_url:
                uid = chat_url.split('&uid=')[1].split('&')[0]
            get_session = self.get_session(session_id, uid)
            if get_session and get_session.user.is_verified:
                self.scope["user"] = get_session.user
            else:
                self.scope['user'] = AnonymousUser()
        except Exception as e:
            logger.error(
                str(e),
                stack_info=True,
                stacklevel=2,
                exc_info=True,
            )

    def get_user(self):
        """
        Get the authenticated user from the scope.
        
        Returns:
            User: Authenticated user.
        """
        return self.scope["user"]

    def get_user_instance(self, **kwargs):
        """
        Get a user instance based on the provided filter criteria.
        
        Args:
            kwargs (dict): Filter criteria for the user instance.
        
        Returns:
            User: User instance matching the filter criteria.
        """
        return get_user_model().objects.get(**kwargs)

    def get_conversation(self, conversation_id):
        """
        Get or create a conversation based on the provided conversation ID.
        
        Args:
            conversation_id (str): ID of the conversation.
        
        Returns:
            Conversation: Conversation object.
        """
        conversation, created = Conversation.objects.get_or_create(id=conversation_id)
        if created:
            chat_user = self.get_user_instance(agent_id=conversation_id)
            self.add_participants(conversation, chat_user)
            # add the user to the conversation
            pass
        return conversation


class ChatConsumer(BaseConsumer):
    """
    Websocket consumer for handling chat functionality.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.conversation_group_name = None
        self.conversation = None
        self.conversation_id = None

    def connect(self):
        """
        Connects the consumer to the WebSocket.
        """
        if self.scope["user"].is_anonymous:
            self.authenticate()

        chat_url = self.scope['query_string'].decode()
        if 'conversation_id=' in chat_url:
            self.conversation_id = chat_url.split('conversation_id=')[1].split('&')[0]
        elif '&conversation_id=' in chat_url:
            self.conversation_id = chat_url.split('&conversation_id=')[1].split('&')[0]

        if self.conversation_id:
            if Conversation.all_objects.filter(id=self.conversation_id).filter(is_removed=True).exists():
                Conversation.all_objects.filter(id=self.conversation_id).filter(is_removed=True).update(is_removed=False)
            
            conversations = Conversation.objects.filter(id=self.conversation_id)
            if conversations.exists():
                self.conversation_id = conversations.first().id
                self.conversation = conversations.first()
                    
        user_id = None
        if 'user_id=' in chat_url:
            user_id = chat_url.split('user_id=')[1].split('&')[0]
        elif '&user_id=' in chat_url:
            user_id = chat_url.split('&user_id=')[1].split('&')[0]

        if user_id:
            user_instance = User.objects.get(id=user_id)
            if self.scope["user"] != user_instance:
                user_list = [self.scope["user"], user_instance]
                if Conversation.all_objects.filter(chat_user=self.scope["user"]).filter(chat_user=user_instance).filter(
                        is_removed=True).exists():
                    Conversation.all_objects.filter(chat_user=self.scope["user"]).filter(chat_user=user_instance).filter(
                        is_removed=True).update(is_removed=False)

                conversations = Conversation.objects.filter(chat_user=self.scope["user"]).filter(chat_user=user_instance)
                if conversations.exists():
                    self.conversation_id = conversations.first().id
                    self.conversation = conversations.first()
                else:
                    conversation = Conversation.objects.create()
                    conversation.chat_user.add(self.scope["user"], user_instance)
                    conversation.save()
                    self.conversation_id = conversation.id
                    self.conversation = conversation

        self.conversation_group_name = f'chat_{self.conversation_id}'

        user = self.scope["user"]
        if user.is_anonymous:
            self.close()
        else:
            async_to_sync(self.channel_layer.group_add)(
                self.conversation_group_name,
                self.channel_name
            )
            self.accept()

    def disconnect(self, close_code):
        """
        Disconnects the consumer from the WebSocket.
        """
        self.channel_layer.group_discard(
            self.conversation_group_name,
            self.channel_name
        )

    def receive_json(self, content):
        """
        Handles incoming JSON data from the WebSocket.
        """
        event_type = content.get('event_type', 'receive_message')
        chat_message = self.create_chat_message(content)

        async_to_sync(self.channel_layer.group_send)(
            self.conversation_group_name,
            {
                "type": "chat.message",
                "content": ChatMessageSerializer(chat_message).data,
                "sender_channel_name": self.channel_name,
            }
        )

    def chat_message(self, event):
        """
        Sends the chat message to the WebSocket.
        """
        message = event["content"]

        self.send_json(content=message)

        async_to_sync(self.channel_layer.group_send)(
            "chat_activity",
            {
                "type": "update_conversation",
                "content": ConversationSerializer(Conversation.objects.filter(chat_user=self.scope["user"]).filter(~Q(last_message=None)),
                                                  many=True, context={'user': self.scope["user"]}).data,
                "sender_channel_name": self.channel_name,
            }
        )

    def create_chat_message(self, content):
        """
        Creates a new chat message object.
        """
        content_type = content.get("content_type", "text")
        chat_message = ChatMessage.objects.create(
            user=self.get_user(),
            conversation=self.conversation,
            message=content.get("message", ""),
            content_type=content_type,
        )

        if content_type != "text":
            media_id = content.get("message_attachment").get("id")
            media = Media.objects.get(id=media_id)
            chat_message.attachment = media
            chat_message.save()

        return chat_message


class ChatActivityConsumer(BaseConsumer):
    """
    This class represents a consumer for chat activity.

    Attributes:
        chat_group_name (str): The name of the chat group.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.chat_group_name = None

    def connect(self):
        """
        Connects the consumer to the chat group and performs authentication if necessary.
        """
        self.chat_group_name = 'chat_activity'
        if self.scope["user"] == AnonymousUser():
            self.authenticate()
        user = self.scope["user"]
        async_to_sync(self.channel_layer.group_add)(
            self.chat_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        """
        Disconnects the consumer from the chat group.
        """
        self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    def change_status(self, event):
        """
        Handles the "change_status" event by updating the user's online status and sending the event data as JSON.
        
        Args:
            event (dict): The event data.
        """
        user_instance = self.get_user_instance(id=event["user_id"])
        user_instance.online_status = event["status"]
        user_instance.save()
        self.send_json(content=event)

    def update_conversation(self, event):
        """
        Handles the "update_conversation" event by sending the event data as JSON.
        
        Args:
            event (dict): The event data.
        """
        self.send_json(content=event)