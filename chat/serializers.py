from users.models import User
from django.db.models import Q
from rest_framework import serializers
# from core.serializers import MediaSerializer, Media
from .models import ChatMessage, Conversation
from employers.models import BlackList
from project_meta.models import Media


class ChatMessageSerializer(serializers.ModelSerializer):
    # message_attachment = MediaSerializer()
    # chat_user = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    conversation = serializers.SerializerMethodField()
    attachment = serializers.SerializerMethodField()

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
            'created'
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
        conversation['id'] = str(obj.conversation.id)
        conversation['last_message'] = str(obj.conversation.last_message.message)
        return conversation

    def get_attachment(self, obj):
        attachment = dict()
        if obj.attachment:
            attachment['id'] = str(obj.attachment.id)
            attachment['title'] = obj.attachment.title
            attachment['type'] = obj.attachment.media_type
            attachment['url'] = str(obj.attachment.file_path.url)
        return attachment

    # def get_chat_user(self, obj):
    #     return ConversationParticipantSerializer(obj.conversation.chat_user).data


class ChatUserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    is_blacklisted = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'email',
            'image',
            'is_blacklisted'
        )

    def get_image(self, obj):
        context = {}
        if obj.image:
            context['id'] = str(obj.image.id)
            context['title'] = obj.image.title
            if obj.image.title == "profile image":
                context['path'] = str(obj.image.file_path)
            else:
                context['path'] = obj.image.file_path.url
            context['type'] = obj.image.media_type
            return context
        return None

    def get_is_blacklisted(self, obj):
        is_blacklisted_record = False
        is_blacklisted_record = BlackList.objects.filter(
            blacklisted_user=obj
        ).exists()
        return is_blacklisted_record


class ConversationSerializer(serializers.ModelSerializer):
    chat_user = serializers.SerializerMethodField()
    last_message = ChatMessageSerializer()

    class Meta:
        model = Conversation
        fields = [
            'id', 'last_message', 'chat_user',
        ]
        
    def get_chat_user(self, obj):
        context = []
        if 'user' in self.context:
            user = self.context['user']
            user_data = obj.chat_user.filter(~Q(id=user.id))
            get_data = ChatUserSerializer(user_data, many=True)
            if get_data.data:
                context = get_data.data
        return context

    # def get_unread_counts(self, obj):
    #     # user = self.context["request"].user
    #     return 0


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
            content_type = str(self.validated_data['attachment'].content_type).split("/")
            if content_type[0] not in ["video", "image"]:
                media_type = 'document'
            else:
                media_type = content_type[0]
            # save media file into media table and get instance of saved data.
            media_instance = Media(title=self.validated_data['attachment'].name,
                                   file_path=self.validated_data['attachment'],
                                   media_type=media_type)
            media_instance.save()
        return {
            'id':str(media_instance.id),
            'title':media_instance.title,
            'media_type':media_instance.media_type,
            'path':media_instance.file_path.url
        }