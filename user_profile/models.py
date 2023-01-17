from django.db import models
from django.utils.translation import gettext as _

from core.models import (
    BaseModel, SoftDeleteModel
)
from users.models import User
from project_meta.models import (
    EducationLevel,
)


class JobSeekerProfile(BaseModel, SoftDeleteModel, models.Model):
    GENDER_CHOICE = (
        ('male', "Male"),
        ('female', "Female"),
    )
    EMPLOYMENT_STATUS_CHOICE = (
        ('employed', "Employed"),
        ('other', "Other"),
        ('fresher', "Fresher"),
    )
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)sJobSeeker'
    )
    gender = models.CharField(
        verbose_name=_('Gender'),
        max_length=255,
        db_column="gender",
        choices=GENDER_CHOICE,
        blank=True,
        null=True,
    )
    dob = models.DateField(
        verbose_name=_('Date of Birth'),
        blank=True,
        null=True,
        default='dob'
    )
    employment_status = models.CharField(
        verbose_name=_('Employment Status'),
        max_length=255,
        db_column="employment_status",
        choices=EMPLOYMENT_STATUS_CHOICE,
        default='employment_status'
    )
    description = models.TextField(
        verbose_name=_('Description'),
        null=True,
        blank=True,
        db_column="description",
    )
    highest_education = models.ForeignKey(
        EducationLevel,
        verbose_name=_('Highest Education'),
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)sHighestEducations'
    )
    market_information_notification = models.BooleanField(
        verbose_name=_('Market Information Notification'),
        db_column="market_information_notification",
        default=True
    )
    job_notification = models.BooleanField(
        verbose_name=_('Job Notification'),
        db_column="job_notification",
        default=True
    )

    def __str__(self):
        return str(self.user) + "(" + str(self.employment_status) + ")"

    class Meta:
        verbose_name = "Job Seeker Profile"
        verbose_name_plural = "Job Seeker Profiles"
        db_table = "JobSeekerProfile"
