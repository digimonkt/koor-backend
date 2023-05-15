from django.db import models
from django.utils.translation import gettext as _

from core.models import (
    BaseModel, SoftDeleteModel
)
from project_meta.models import (
    Media
)
from users.models import (
    TimeStampedModel, User
)


class Conversation(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    The Conversation model represents a conversation between two or more users.

    Attributes:
        - last_message (ForeignKey): A foreign key that references the last message in the conversation. This field
            is nullable, meaning that it can be empty, and is set to null when the last message is deleted.

    Meta:
        - verbose_name (str): A human-readable name for the model used in the Django admin interface.
        - verbose_name_plural (str): A human-readable plural name for the model used in the Django admin interface.
        - db_table (str): The name of the database table that stores the model's data.
        - ordering (list): A list of field names used to order the Conversation objects in ascending or descending
            order of creation time. In this case, the Conversation objects will be ordered in descending order of creation time.

    Inheritance:
        The Conversation model inherits from the following four models:

        - BaseModel: Provides fields like id, created_at, updated_at.
        - SoftDeleteModel: Provides a field named is_deleted, which is a flag indicating whether the object
            has been soft-deleted.
        - TimeStampedModel: Provides fields named created and modified, which are set to the date and time the
            object was created and last modified, respectively.
        - models.Model: The base class for Django models.

    Usage:
        The Conversation model can be used to store information about conversations between users in a chat
        application. You can retrieve and manipulate the data using the Django ORM or the Django admin interface.

    """

    last_message = models.ForeignKey(
        to="chat.ChatMessage",
        verbose_name=_("Last Message"),
        related_name="+",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
        db_table = "Conversation"
        ordering = ['-created']


class ConversationUser(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    The ConversationUser model represents the relationship between a user and a conversation in a chat application.

    Attributes:
        - user (ForeignKey): A foreign key that references the user who is a participant in the conversation.
        - conversation (ForeignKey): A foreign key that references the conversation in which the user is participating.

    Meta:
        - verbose_name (str): A human-readable name for the model used in the Django admin interface.
        - verbose_name_plural (str): A human-readable plural name for the model used in the Django admin interface.
        - db_table (str): The name of the database table that stores the model's data.
        - ordering (list): A list of field names used to order the ConversationUser objects in ascending or
            descending order of creation time. In this case, the ConversationUser objects will be ordered in
            descending order of creation time.

    Inheritance:
        The ConversationUser model inherits from the following four models:
        - BaseModel: Provides fields like id, created_at, updated_at.
        - SoftDeleteModel: Provides a field named is_deleted, which is a flag indicating whether the object has
            been soft-deleted.
        - TimeStampedModel: Provides fields named created and modified, which are set to the date and time the object
            was created and last modified, respectively.
        - models.Model: The base class for Django models.

    Usage:
        The ConversationUser model can be used to represent the relationship between a user and a conversation in a
        chat application. You can retrieve and manipulate the data using the Django ORM or the Django admin interface.

    """

    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)s_user'
    )
    conversation = models.ForeignKey(
        Conversation,
        verbose_name=_('Conversation'),
        on_delete=models.CASCADE,
        db_column="conversation",
        related_name='%(app_label)s_%(class)s_conversations'
    )

    class Meta:
        verbose_name = "Conversation User"
        verbose_name_plural = "Conversation Users"
        db_table = "ConversationUser"
        ordering = ['-created']


class ChatMessage(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    The ChatMessage model represents a message in a conversation in a chat application.

    Attributes:
        - user (ForeignKey): A foreign key that references the user who sent the message.
        - conversation (ForeignKey): A foreign key that references the conversation in which the message was sent.
        - message (TextField): The text of the message.
        - attachment (OneToOneField): A foreign key that references the media attachment associated with the message.
        - is_seen (BooleanField): A boolean field that indicates whether the message has been seen by the recipient.
        - is_edited (BooleanField): A boolean field that indicates whether the message can be edited by the sender.

    Meta:
        - verbose_name (str): A human-readable name for the model used in the Django admin interface.
        - verbose_name_plural (str): A human-readable plural name for the model used in the Django admin interface.
        - db_table (str): The name of the database table that stores the model's data.
        - ordering (list): A list of field names used to order the ChatMessage objects in ascending or descending
            order of creation time. In this case, the ChatMessage objects will be ordered in descending order of
            creation time.

    Inheritance:
        The ChatMessage model inherits from the following four models:
        - BaseModel: Provides fields like id, created_at, updated_at.
        - SoftDeleteModel: Provides a field named is_deleted, which is a flag indicating whether the object has
            been soft-deleted.
        - TimeStampedModel: Provides fields named created and modified, which are set to the date and time the
            object was created and last modified, respectively.
        - models.Model: The base class for Django models.

    Usage:
        The ChatMessage model can be used to represent a message in a conversation in a chat application. You
        can retrieve and manipulate the data using the Django ORM or the Django admin interface.

    """

    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)s_user'
    )
    conversation = models.ForeignKey(
        Conversation,
        verbose_name=_('Conversation'),
        on_delete=models.CASCADE,
        db_column="conversation",
        related_name='%(app_label)s_%(class)s_conversations'
    )
    message = models.TextField(
        verbose_name=_('Message'),
        null=True,
        blank=True,
        db_column="message",
    )
    attachment = models.OneToOneField(
        Media,
        verbose_name=_('Attachment'),
        on_delete=models.CASCADE,
        db_column="attachment",
        related_name='%(app_label)s_%(class)s_attachment'
    )
    is_seen = models.BooleanField(
        verbose_name=_('Is Seen'),
        default=False,
        db_column="is_seen",
    )
    is_edited = models.BooleanField(
        verbose_name=_('Is Edited'),
        default=False,
        db_column="is_edited",
    )

    class Meta:
        verbose_name = "Chat Message"
        verbose_name_plural = "Chat Messages"
        db_table = "ChatMessage"
        ordering = ['-created']
