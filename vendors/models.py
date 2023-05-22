from django.db import models
from django.utils.translation import gettext as _

from core.models import BaseModel, SoftDeleteModel

from users.models import User, TimeStampedModel

from tenders.models import TenderDetails

from project_meta.models import (
    Media
)


class SavedTender(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    This is a Django model for a Saved Tender object, associated with a vendor user, with the following fields:

    - `user`: the user associated with the saved tender
    - `tender`: the tender associated with the saved tender
    """
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)s_users'
    )
    tender = models.ForeignKey(
        TenderDetails,
        verbose_name=_('Tender'),
        on_delete=models.CASCADE,
        db_column="tender",
        related_name='%(app_label)s_%(class)s_tenders'
    )
    notified = models.BooleanField(
        verbose_name=_('Notified'),
        null=True,
        blank=True,
        db_column="notified",
        default=False
    )

    def __str__(self):
        return str(self.tender) + "(" + str(self.user) + ")"

    class Meta:
        verbose_name = "Saved Tender"
        verbose_name_plural = "Saved Tenders"
        db_table = "SavedTender"
        ordering = ['-created']


class AppliedTender(BaseModel, TimeStampedModel, models.Model):
    """
    Model representing an applied tender.

    Attributes:
        - user (ForeignKey): The user who applied for the tender.
        - tender (ForeignKey): The tender details for which the user applied.
        - shortlisted_at (DateTimeField): The datetime when the user was shortlisted for the tender.
        - rejected_at (DateTimeField): The datetime when the user was rejected for the tender.
        - short_letter (TextField): The short letter submitted by the user while applying for the tender.

    Methods:
        __str__: Returns a string representation of the applied tender.

    Meta:
        - verbose_name (str): Singular name for the model in the admin interface.
        - verbose_name_plural (str): Plural name for the model in the admin interface.
        - db_table (str): Name of the database table for the model.
        - ordering (list): List of fields to use for default ordering of instances.
    """

    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)s_user'
    )
    tender = models.ForeignKey(
        TenderDetails,
        verbose_name=_('Tender'),
        on_delete=models.CASCADE,
        db_column="tender",
        related_name='%(app_label)s_%(class)s_tender'
    )
    shortlisted_at = models.DateTimeField(
        verbose_name=_('Short Listed At'),
        null=True,
        blank=True,
        db_column="shortlisted_at"
    )
    rejected_at = models.DateTimeField(
        verbose_name=_('Rejected At'),
        null=True,
        blank=True,
        db_column="rejected_at"
    )
    short_letter = models.TextField(
        verbose_name=_('Short Letter'),
        null=True,
        blank=True,
        db_column="short_letter",
    )

    def __str__(self):
        return str(self.tender) + "(" + str(self.user) + ")"

    class Meta:
        verbose_name = "Applied Tender"
        verbose_name_plural = "Applied Tenders"
        db_table = "AppliedTender"
        ordering = ['-created']


class AppliedTenderAttachmentsItem(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    This is a Django model for an Applied Tender Attachment object, associated with an Applied Tender item, with the following fields:

    - `applied_tender`: the applied tender associated with the attachment
    - `attachment`: the attachments uploaded for the applied tender
    """
    applied_tender = models.ForeignKey(
        AppliedTender,
        verbose_name=_('Applied Tender'),
        on_delete=models.CASCADE,
        db_column="applied_tender",
        null=True,
        related_name='%(app_label)s_%(class)s_applied_tender'
    )
    attachment = models.OneToOneField(
        Media,
        verbose_name=_('Attachment'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="attachment",
        related_name='%(app_label)s_%(class)s_attachment'
    )

    def __str__(self):
        return str(self.applied_tender)

    class Meta:
        verbose_name = "Applied Tender Attachment Item"
        verbose_name_plural = "Applied Tender Attachment Items"
        db_table = "AppliedTenderAttachmentsItem"
        ordering = ['-created']
