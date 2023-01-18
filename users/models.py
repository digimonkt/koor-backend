from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from core.models import (
    BaseModel, SoftDeleteModel
)
from project_meta.models import Media

from .managers import UserManager


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
        verbose_name=_('Email Address'),
        blank=True,
        null=True,
        db_column="email"
    )
    mobile_number = models.CharField(
        verbose_name=_('Mobile Number'),
        max_length=13,
        blank=True,
        null=True,
        db_column="mobile_number"
    )
    country_code = models.CharField(
        verbose_name=_('Country Code'),
        max_length=250,
        blank=True,
        null=True,
        db_column="country_code"
    )
    display_name = models.CharField(
        verbose_name=_('Display Name'),
        max_length=250,
        blank=True,
        null=True,
        db_column="display_name"
    )
    profile_role = models.CharField(
        verbose_name=_('Profile Role'),
        max_length=250,
        blank=True,
        null=True,
        db_column="profile_role",
        choices=ROLE_TYPE_CHOICE,
        default='admin'
    )
    image = models.ForeignKey(
        Media,
        verbose_name=_('Image'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        db_column="image",
        related_name='%(app_label)s_%(class)s_image'
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


class UserSession(BaseModel, SoftDeleteModel, models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)s_user'
    )
    ip_address = models.GenericIPAddressField(
        verbose_name=_('IP Address'),
        protocol='both',
        unpack_ipv4=False,
        null=True,
        blank=True,
        db_column="ip_address"
    )
    agent = models.JSONField(
        verbose_name=_('Agent'),
        null=True,
        db_column="agent"
    )
    expire_at = models.DateTimeField(
        verbose_name=_('Expire At'),
        blank=True,
        null=True,
        db_column="expire_at"

    )

    def __str__(self):
        return str(self.ip_address) + "(" + str(self.agent) + ")"

    class Meta:
        verbose_name = "User Session"
        verbose_name_plural = "User Sessions"
        db_table = "UserSession"
