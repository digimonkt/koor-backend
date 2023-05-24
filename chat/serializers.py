from django.contrib.auth import get_user_model
from rest_framework import serializers
# from core.serializers import MediaSerializer, Media
from .models import ChatMessage, Conversation

from project_meta.models import Media


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


class UploadAttachmentSerializers(serializers.ModelSerializer):

    attachment = serializers.FileField(
        style={"input_type": "file"},
        write_only=True,
        allow_null=False
    )

    class Meta:
        model = Media
        fields = ['attachment']

    def save(self):
        media_instance = None
        if 'attachment' in self.validated_data:
            # Get media type from upload license file
            content_type = str(validated_data['attachment'].content_type).split("/")
            if content_type[0] not in ["video", "image"]:
                media_type = 'document'
            else:
                media_type = content_type[0]
            # save media file into media table and get instance of saved data.
            media_instance = Media(title=validated_data['attachment'].name, file_path=validated_data['attachment'],
                                   media_type=media_type)
            media_instance.save()
        return media_instance
