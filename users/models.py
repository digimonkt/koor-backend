from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from core.models import BaseModel
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
        _('Email Address'),
        blank=True,
        null=True,
    )
    mobile_number = models.CharField(
        _('Mobile Number'),
        max_length=13,
        blank=True,
        null=True,
        db_column="mobile_number"
    )
    country_code = models.CharField(
        _('Country Code'),
        max_length=250,
        blank=True,
        null=True,
        db_column="country_code"
    )
    display_name = models.CharField(
        _('Display Name'),
        max_length=250,
        blank=True,
        null=True,
        db_column="display_name"
    )
    profile_role = models.CharField(
        _('Profile Role'),
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
        related_name='%(app_label)s_%(class)s'
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
