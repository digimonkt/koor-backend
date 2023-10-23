from rest_framework import serializers

from employers.models import BlackList
from project_meta.models import Media
from users.models import User
from .models import ChatMessage, Conversation


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model, providing a custom method to retrieve the user's image.

    Attributes:
        image (SerializerMethodField): A serializer field representing the user's image.

    Meta:
        model (User): The User model class to be serialized.
        fields (list): A list of fields to include in the serialized representation.

    Methods:
        get_image(obj): Returns the URL or file path of the user's image.
            Args:
                obj (User): The User instance being serialized.
            Returns:
                str or None: The URL or file path of the user's image, or None if it doesn't exist.
    """

    image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'email',
            'image'
        ]

    def get_image(self, obj):
        image = None
        if obj.image:
            if obj.image.title == "profile image":
                image = str(obj.image.file_path)
            else:
                image = obj.image.file_path.url
        return image


class GetConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving conversations with the last message.

    Attributes:
        last_message (serializers.SerializerMethodField): Field to retrieve the last message in the conversation.

    Meta:
        model (Conversation): The Conversation model to serialize.
        fields (list): The fields to include in the serialized representation, including 'id' and 'last_message'.

    Methods:
        get_last_message(obj): Method to retrieve the message from the last message object in the conversation.

    """

    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'id',
            'last_message',
        ]

    def get_last_message(self, obj):
        """
        Retrieve the message from the last message object in the conversation.

        Args:
            obj (Conversation): The Conversation object being serialized.

        Returns:
            str: The message content from the last message in the conversation.

        """

        return obj.last_message.message


class AttachmentSerializer(serializers.ModelSerializer):
    """
    Serializes the `Media` model fields for attachment data.

    This serializer is used to convert the `Media` model fields into a JSON representation
    for attachment data. It specifies the model, `Media`, and the fields to be included
    in the serialized output.

    Attributes:
        model (class): The model class that the serializer is based on.
        fields (list): The list of fields from the `Media` model to be serialized.

    Example:
        serializer = AttachmentSerializer(data)
        serialized_data = serializer.data

    """
    type = serializers.SerializerMethodField()
    path = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = [
            'id',
            'title',
            'type',
            'path'
        ]

    def get_type(self, obj):
        return obj.media_type

    def get_path(self, obj):
        return obj.file_path.url


class ChatMessageSerializer(serializers.ModelSerializer):
    """
    Serializes a ChatMessage object into a JSON representation.

    Attributes:
        user (UserSerializer): Serializer for the User object associated with the message.
        conversation (GetConversationSerializer): Serializer for the Conversation object associated with the message.
        attachment (AttachmentSerializer): Serializer for the Attachment object associated with the message.

    Meta:
        model (ChatMessage): The model class for the serializer.
        fields (list): The fields to include in the serialized representation.

    Example usage:
        serializer = ChatMessageSerializer(data=chat_message_data)
        if serializer.is_valid():
            serialized_data = serializer.data
            # Further processing or response handling
        else:
            # Error handling for invalid data
    """

    user = UserSerializer()
    conversation = GetConversationSerializer()
    attachment = AttachmentSerializer()
    reply_to = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = [
            'reply_to',
            'user',
            'conversation',
            'message',
            'attachment',
            'is_seen',
            'is_edited',
            'id',
            'created'
        ]
        
    def get_reply_to(self, obj):
        if obj.reply_to:
            return {
                'id': obj.reply_to.id,
                'message': obj.reply_to.message,
                'user': obj.reply_to.user,
                'created': obj.reply_to.created,
            }
        else:
            return {}


class ChatUserSerializer(serializers.ModelSerializer):
    """
    Serializer for ChatUser objects.

    Serializes the ChatUser model fields, including additional fields for 'image' and 'is_blacklisted'. The 'image'
    field is a dictionary representing the associated image details if it exists, or None otherwise.
    The 'is_blacklisted' field indicates whether the user is blacklisted or not.

    Serializer Fields:
        - id: User's ID
        - name: User's name
        - email: User's email
        - image: Dictionary containing image details (id, title, path, type)
                 or None if no image is associated with the user.
        - is_blacklisted: Boolean indicating whether the user is blacklisted or not.

    """

    image = serializers.SerializerMethodField()
    is_blacklisted = serializers.SerializerMethodField()
    blacklisted = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'email',
            'image',
            'is_blacklisted',
            'blacklisted'
        )

    def get_image(self, obj):
        """
        Get the image details for the user.

        Parameters:
            - obj: ChatUser instance

        Returns:
        - Dictionary containing the image details (id, title, path, type) if an image exists, or None if no image is
            associated with the user.
        """

        if obj.image:
            image = obj.image
            context = {
                'id': str(image.id),
                'title': image.title,
                'path': str(image.file_path) if image.title == "profile image" else image.file_path.url,
                'type': image.media_type
            }
            return context
        return None

    def get_is_blacklisted(self, obj):
        """
        Check if the user is blacklisted.

        Parameters:
            - obj: ChatUser instance

        Returns:
            - Boolean indicating whether the user is blacklisted (True) or not (False).
        """

        return BlackList.objects.filter(blacklisted_user=obj).exists()

    def get_blacklisted(self, obj):
        user = self.context.get('user')
        if user:
            return BlackList.objects.filter(user=obj).filter(blacklisted_user=user).exists()
        return None


class ConversationSerializer(serializers.ModelSerializer):
    chat_user = serializers.SerializerMethodField()
    last_message = ChatMessageSerializer()

    class Meta:
        model = Conversation
        fields = ['id', 'last_message', 'chat_user']

    def get_chat_user(self, obj):
        """
        Retrieve the serialized data of chat users associated with the conversation, excluding the current user.

        Args:
            - obj: The Conversation instance for which to retrieve chat users.

        Returns:
            - list: A list of serialized chat user data.

        Notes:
            The chat users are filtered to exclude the current user, if available in the serializer's context.
            If there are no chat users available or the current user is not provided in the context, an empty list is
            returned.
        """

        user = self.context.get('user')
        if user:
            user_data = obj.chat_user.exclude(id=user.id)
            if user_data.exists():
                return ChatUserSerializer(user_data, many=True, context={'user': user}).data
        return []


class UploadAttachmentSerializers(serializers.ModelSerializer):
    """
    Serializer for uploading attachments and saving them as Media instances.

    Attributes:
        attachment (FileField): File field representing the attachment file.

    Meta:
        model (Media): The Media model to be used for saving the attachment.
        fields (list): List of fields to be serialized.

    Methods:
        save(): Save the attachment file as a Media instance.

    """

    attachment = serializers.FileField(
        style={"input_type": "file"},
        write_only=True,
        allow_null=False
    )

    class Meta:
        model = Media
        fields = ['attachment']

    def save(self):
        """
        Save the attachment file as a Media instance.

        Returns:
            dict or None: A dictionary containing information about the saved Media instance, including 'id', 'title',
                            'media_type', and 'path'. Returns None if 'attachment' is not found in the validated data.

        """

        if 'attachment' in self.validated_data:
            attachment = self.validated_data['attachment']
            content_type = attachment.content_type.split("/")
            media_type = 'document' if content_type[0] not in ["video", "image"] else content_type[0]
            media_instance = Media.objects.create(
                title=attachment.name,
                file_path=attachment,
                media_type=media_type
            )
            return {
                'id': str(media_instance.id),
                'title': media_instance.title,
                'media_type': media_instance.media_type,
                'path': media_instance.file_path.url
            }
        return None
