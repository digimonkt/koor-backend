from django.contrib.auth import get_user_model
from rest_framework import serializers
# from core.serializers import MediaSerializer, Media
from .models import ChatMessage, Conversation


class ChatMessageSerializer(serializers.ModelSerializer):
    # message_attachment = MediaSerializer()
    # chat_user = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    conversation = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = [
            'user',
            'conversation',
            'message',
            'attachment',
            'is_seen',
            'is_edited',
            'id',

        ]

    def get_user(self, obj):
        user = dict()
        user['id'] = str(obj.user.id)
        user['name'] = obj.user.name
        user['email'] = obj.user.email
        if obj.user.image:
            if obj.user.image.title == "profile image":
                user['image'] = str(obj.user.image.file_path)
            else:
                user['image'] = obj.user.image.file_path.url
        return user

    def get_conversation(self, obj):
        conversation = dict()
        print("I am here")

        conversation['id'] = str(obj.conversation.id)
        conversation['last_message'] = str(obj.conversation.last_message.id)
        return conversation

    # def get_chat_user(self, obj):
    #     return ConversationParticipantSerializer(obj.conversation.chat_user).data


# class ConversationParticipantSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = get_user_model()
#         fields = [
#             'id',
#             'agent_id', 'online_status', 'full_name',
#         ]

class ConversationSerializer(serializers.ModelSerializer):
    # chat_user = ConversationParticipantSerializer()
    # members = ConversationParticipantSerializer(many=True, read_only=True)
    last_message = ChatMessageSerializer()
    unread_counts = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'id', 'last_message', 'unread_counts',
        ]

    def get_unread_counts(self, obj):
        # user = self.context["request"].user
        return 0

# class ChatMetaSerializer(serializers.ModelSerializer):
#     unread_counts = serializers.SerializerMethodField()
#     class Meta:
#         model = Conversation
#         fields = ['unread_counts',]

#     def get_unread_counts(self, obj):
#         user = self.context["request"].user
#         return obj.get_unread_messages(user).count()
