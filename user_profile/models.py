from django.db import models
from django.utils.translation import gettext as _
from users.models import User
from core.models import BaseModel


class UserProfile(BaseModel, models.Model):
    GENDER_CHOICE = (
        ('male', "Male"),
        ('female', "Female"),
    )
    EMPLOYMENT_STATUS_CHOICE = (
        ('employed', "Employed"),
        ('fresher', "Fresher"),
        ('other', "Other"),
    )
    user = models.OneToOneField(
        User,
        verbose_name=_('User'),
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)sSession'
    )
    gender = models.CharField(
        verbose_name=__('Employment Status'),
        max_length=250,
        blank=True,
        null=True,
        db_column="media_type",
        choices=GENDER_CHOICE,
        default='image'
    )
    dob = models.DateField(
        verbose_name=_('Date of Birth'),
        null=True,
        blank=True,
        db_column="dob",
    )
    employment_status = models.CharField(
        verbose_name=__('Employment Status'),
        max_length=250,
        blank=True,
        null=True,
        db_column="employment_status",
        choices=EMPLOYMENT_STATUS_CHOICE,
    )
    description = models.TextField(
        verbose_name=_('Description'),
        null=True,
        blank=True,
        db_column="description",
    )
    market_information = models.BooleanField(
        verbose_name=_('Market Information'),
        default=False,
        blank=True,
        null=True,
        db_column="market_information",
    )
    job_notification = models.BooleanField(
        verbose_name=_('Job Notification'),
        default=False,
        blank=True,
        null=True,
        db_column="job_notification",
    )

    active = models.BooleanField(
        verbose_name=_('Active'),
        default=True,
        blank=True,
        null=True,
        db_column="active",
    )

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        db_table = "UserProfile"

