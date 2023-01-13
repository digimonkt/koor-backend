import logging

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from core.exceptions import UserNotPassed
from core.models import BaseModel
from .managers import UserManager
from project_meta.models import Media


# Create Auth User Model Start
class User(AbstractUser, BaseModel):
    ROLE_TYPE_CHOICE = (
        ('admin', "Admin"),
        ('job_seeker', "Job Seeker"),
        ('employer', "Employer"),
        ('vendor', "Vendor"),
    )

    username = None
    first_name = None
    last_name = None
    email = models.EmailField(
        _('Email Address'),
        blank=True,
        null=True,
    )
    mobile = models.CharField(
        _('Mobile Number'),
        max_length=13,
        blank=True,
        null=True,
        db_column="mobile_number"
    )
    display_name = models.CharField(
        _('Full Name'),
        max_length=250,
        blank=True,
        null=True,
        db_column="display_name"
    )
    profile_role = models.CharField(
        _('Role'),
        max_length=250,
        blank=True,
        null=True,
        db_column="profile_role",
        choices=ROLE_TYPE_CHOICE,
        default='admin'
    )
    address = models.TextField(
        _('Address'),
        blank=True,
        null=True,
        db_column="address"
    )
    country_code = models.CharField(
        _('Country Code'),
        max_length=13,
        blank=True,
        null=True,
        db_column="country_code"
    )
    image = models.ForeignKey(
        Media,
        verbose_name=_('Created By'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)sCreatedBy'
    )
    USERNAME_FIELD = 'email'  # set email as a username
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(self.id)  # return value when call model as primary key

    class Meta:
        verbose_name = "User"  # display table name
        verbose_name_plural = "Users"  # display table name as plural
        db_table = 'User'  # table name in DB


class UserStampedModel(models.Model):
    """
    An abstract base class model that provides self updating ``created_by`` and ``updated_by`` fields.
    """
    _user_model = User

    created_by = models.ForeignKey(
        _user_model,
        verbose_name=_('Created By'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)sCreatedBy'
    )
    updated_by = models.ForeignKey(
        _user_model,
        verbose_name=_('Updated By'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)sUpdatedBy",
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        logger = logging.getLogger(__name__)
        try:
            if "user" in kwargs:
                user = kwargs.pop("user")

                if self.created_by is None:
                    self.created_by = user
                else:
                    self.updated_by = user
            else:
                # If user object is not passed to save method we raise the KeyError
                raise UserNotPassed

            return super().save()

        except UserNotPassed:
            # If we have UserNotPassed then we generate a warning
            # cause various admin panel request make call to the .save() implicitly.
            logger.warning('User object is not passed!')

        except Exception as e:
            logger.exception(e, exc_info=True)


class UserSession(BaseModel, models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)sSession'
    )
    ip_address = models.GenericIPAddressField(
        verbose_name=_('IP Address'),
        protocol='both',
        unpack_ipv4=False,
        null=True,
        blank=True,
    )
    agent = models.JSONField(
        verbose_name=_('Agent'),
        null=True,
    )
    expire_at = models.DateTimeField(
        verbose_name=_('Created At'),
        blank=True,
        null=True
    )
    active = models.BooleanField(
        verbose_name=_('Active'),
        default=True,
        blank=True,
        null=True
    )
    deleted = models.BooleanField(
        verbose_name=_('Deleted'),
        default=False,
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.ip_address) + "(" + str(self.agent) + ")"

    class Meta:
        verbose_name = "User Session"
        verbose_name_plural = "User Sessions"
        db_table = "UserSession"
