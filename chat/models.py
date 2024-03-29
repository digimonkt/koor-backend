from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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
    Represents a conversation between multiple users.

    Attributes:
        - `chat_user (ManyToManyField)`: A many-to-many relationship field that represents the users participating in
            the conversation.
        - `last_message (ForeignKey)`: A foreign key field that refers to the last message sent in the conversation.

    Meta:
        - `verbose_name (str)`: The human-readable name for a single instance of the model.
        - `verbose_name_plural (str)`: The human-readable name for the model in plural form.
        - `db_table (str)`: The name of the database table associated with the model.
        - `ordering (list)`: The default ordering for querysets of this model.
    """

    chat_user = models.ManyToManyField(
        User,
        verbose_name=_('User'),
        db_column="user",
        related_name='%(app_label)s_%(class)s_user'
    )
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
        ordering = ['-modified']


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
    reply_to = models.ForeignKey(
        'self',
        verbose_name=_('Reply To'),
        on_delete=models.SET_NULL,
        db_column="reply_to",
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)s_reply_to'
    )
    attachment = models.OneToOneField(
        Media,
        verbose_name=_('Attachment'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        db_column="attachment",
        related_name='%(app_label)s_%(class)s_attachment'
    )
    is_seen = models.BooleanField(
        verbose_name=_('Is Seen'),
        default=False,
        db_column="is_seen",
    )
    read_by = models.ManyToManyField(
        to=User,
        verbose_name=_('Read By'),
        related_name='%(app_label)s_%(class)s_read_by',
        blank=True,
        null=True,
        db_column="read_by",
    )
    is_edited = models.BooleanField(
        verbose_name=_('Is Edited'),
        default=False,
        db_column="is_edited",
    )
    content_type = models.CharField(
        verbose_name=_("Content Type"),
        db_column="content_type",
        max_length=255,
        editable=False,
        default="text",
    )

    class Meta:
        verbose_name = "Chat Message"
        verbose_name_plural = "Chat Messages"
        db_table = "ChatMessage"
        ordering = ['-created']


@receiver(post_save, sender=ChatMessage)
def update_last_message(sender, instance, created, **kwargs):
    """
    Signal handler to update the last message of a conversation when a new ChatMessage instance is created.

    Args:
        sender (Type[ChatMessage]): The model class that sent the signal (ChatMessage).
        instance (ChatMessage): The instance of the ChatMessage that was saved.
        created (bool): A boolean indicating whether the instance was just created or updated.
        **kwargs: Additional keyword arguments that may be passed by the signal.

    Returns:
        None

    Side Effects:
        Updates the last_message field of the conversation associated with the saved ChatMessage instance.

    """

    if created:
        conversation = instance.conversation
        conversation.last_message = instance
        conversation.save()
