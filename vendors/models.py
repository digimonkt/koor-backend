from django.db import models
from django.utils.translation import gettext as _

from core.models import BaseModel, SoftDeleteModel

from users.models import User, TimeStampedModel

from tenders.models import TenderDetails


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
