from django.db import models
from django.utils.translation import gettext as _

from core.models import (
    BaseModel, SoftDeleteModel
)
from users.models import User, TimeStampedModel


class BlackList(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    This class created for user information who is black listed by employer.
    Here we have some useful field like:- user, blacklisted_user.
        - user is the employer detail field.
        - blacklisted_user is black listed user detail field.
    """
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)s_user'
    )
    blacklisted_user = models.ForeignKey(
        User,
        verbose_name=_('Blacklisted User'),
        on_delete=models.CASCADE,
        db_column="blacklisted_user",
        related_name='%(app_label)s_%(class)s_blacklisted_user'
    )

    def __str__(self):
        return str(self.blacklisted_user)

    class Meta:
        verbose_name = "Black List"
        verbose_name_plural = "Black Lists"
        db_table = "BlackList"
