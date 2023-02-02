from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

from model_utils import models as misc_models

from core.models import (
    BaseModel, SoftDeleteModel
)
from project_meta.models import Media

from .managers import UserManager


# Create Auth User Model Start
class User(AbstractUser, BaseModel, SoftDeleteModel):
    """
    This class created for get detail of all user like: admin, JobSeeker, Employer etc.
    Here we have some useful field like:- email, mobile_number, country_code, name, role, image.
        - we can get all other default authenticate filed in this user model class.
    """
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
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=250,
        blank=True,
        null=True,
        db_column="name"
    )
    role = models.CharField(
        verbose_name=_('Role'),
        max_length=250,
        db_column="role",
        choices=ROLE_TYPE_CHOICE
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

class TimeStampedModel(misc_models.TimeStampedModel, models.Model):
    """
    This abstract base model is used to store timestamps for model creation and modification in a Django Model.

    Columns:
    - `created`: A datetime object representing the creation time of the model.
    - `modified`: A datetime object representing the last modification time of the model.
    - `created_by`: A string representing the user who created the model.
    - `modified_by`: A string representing the user who last modified the model.
    """

    created_by = models.ForeignKey(
        User,
        verbose_name=_('Created By'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_created_by'
    )
    modified_by = models.ForeignKey(
        User,
        verbose_name=_('Modified By'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_modified_by",
    )

    class Meta:
        abstract = True
