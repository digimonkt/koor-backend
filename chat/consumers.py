import logging

import jwt
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

from koor.config.common import Common
from users.models import UserSession, User
from .models import Conversation, ChatMessage
from .serializers import ChatMessageSerializer

# Get JWT secret key
SECRET_KEY = settings.SECRET_KEY


class BaseConsumer(JsonWebsocketConsumer):

    def decode_token(self, token):
        # If the token expired this raise jwt.ExpiredSignatureError
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=['HS256', ])
        return payload

    def get_session(self, payload):
        '''
        Get the session for the given token.
        '''
        try:
            session_id = payload[Common.SIMPLE_JWT.get('USER_ID_CLAIM', 'user_id')]
            session = UserSession.objects.get(id=session_id)
            return session
        except UserSession.DoesNotExist:
            return None

    # TODO: DIY
    def authenticate(self):
        logger = logging.getLogger(__name__)
        headers = dict(self.scope["headers"])
        try:
            if b"authorization" in headers:
                token = headers[b"authorization"].decode("utf-8")
                access_token = token.replace('Bearer ', '')
                validated_token = self.decode_token(access_token)
                get_session = self.get_session(validated_token)
                if get_session.user.is_verified:
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
        return User.objects.get(id='c05dc8d0-f96f-4e37-9fc6-742f3c809c61')
        # return self.scope["user"]

    def get_user_instance(self, **kwargs):
        return User.objects.get(id='c05dc8d0-f96f-4e37-9fc6-742f3c809c61')
        # return get_user_model().objects.get(**kwargs)

    def get_conversation(self, conversation_id):
        conversation, created = Conversation.objects.get_or_create(id=conversation_id)
        if created:
            # add the user to the conversation
            pass
        return conversation


class ChatConsumer(BaseConsumer):

    def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.conversation = self.get_conversation(self.conversation_id)
        self.conversation_group_name = f'chat_{self.conversation.id}'
        if self.scope["user"] == AnonymousUser():
            self.authenticate()
        user = self.scope["user"]
        # if user.is_anonymous:
        #     pass
        #     # self.close()
        # else:
        async_to_sync(self.channel_layer.group_add)(
            self.conversation_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        self.channel_layer.group_discard(
            self.conversation_group_name,
            self.channel_name
        )

    def receive_json(self, content):
        event_type = content.get('event_type', 'receive_message')
        # if event_type == 'delete_message':
        #         messages = ChatMessage.objects.filter(id__in=content.get('id'))
        #         messages.delete()

        #         # Delete message
        #         async_to_sync(self.channel_layer.group_send)(
        #             self.conversation_group_name, 
        #             {
        #                 "type": "delete.message", 
        #                 "sender_channel_name": self.channel_name,
        #                 **content
        #             }
        #         )
        # else:
        # Create the chat message object
        chat_message = self.create_chat_message(content)
        print(chat_message, "chat message")

        print("ChatMessageSerializer", ChatMessageSerializer(chat_message).data)
        # chat_message = ChatMessage.objects.get(id=chat_message)
        # if chat_message:
        #     chat_message.mark_as_read(self.get_user())
        #     chat_message.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.conversation_group_name,
            {
                "type": "chat.message",
                "content": ChatMessageSerializer(chat_message).data,
                "sender_channel_name": self.channel_name,
            }
        )

    def chat_message(self, event):
        # Exclude the sender from receiving the message
        message = "event['message']"
        # Send message to WebSocket
        # if self.channel_name != event["sender_channel_name"]:
        self.send_json(content=event["content"])
        async_to_sync(self.channel_layer.group_send)(
            "chat_activity",
            {
                "type": "update_conversation",
                "content": event["content"],
                "sender_channel_name": self.channel_name,
            }
        )

    def create_chat_message(self, content):
        content_type = content.get("content_type", "text")
        # TODO: Implement the participant filter
        chat_message = ChatMessage.objects.create(
            user=self.get_user(),
            conversation=self.conversation,
            message=content.get("message", ""),
            # content_type=content_type,
        )
        # if content_type != "text":
        #     media_id = int(content.get("message_attachment").get("id"))
        #     media = Media.objects.get(id=media_id)
        #     chat_message.message_attachment = media
        #     chat_message.save()
        return chat_message