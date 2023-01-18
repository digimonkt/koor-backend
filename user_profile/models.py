from django.db import models
from django.utils.translation import gettext as _

from core.models import (
    BaseModel, SoftDeleteModel
)
from users.models import User
from project_meta.models import (
    EducationLevel, Media
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
        related_name='%(app_label)s_%(class)sUser'
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
        db_column='dob'
    )
    employment_status = models.CharField(
        verbose_name=_('Employment Status'),
        max_length=255,
        db_column="employment_status",
        choices=EMPLOYMENT_STATUS_CHOICE,
        default='employed'
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
        null=True,
        blank=True,
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


class EmployerProfile(BaseModel, SoftDeleteModel, models.Model):
    ORGANIZATION_TYPE_CHOICE = (
        ('government', "Government"),
        ('ngo', "NGO"),
        ('business', "Business"),
    )
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)sUser'
    )
    description = models.TextField(
        verbose_name=_('Description'),
        null=True,
        blank=True,
        db_column="description",
    )
    organization_type = models.CharField(
        verbose_name=_('Organization Type'),
        max_length=255,
        db_column="organization_type",
        choices=ORGANIZATION_TYPE_CHOICE,
        blank=True,
        null=True,
    )
    market_information_notification = models.BooleanField(
        verbose_name=_('Market Information Notification'),
        db_column="market_information_notification",
        default=False
    )
    other_notification = models.BooleanField(
        verbose_name=_('Other Notification'),
        db_column="other_notification",
        default=False
    )
    license_id = models.CharField(
        verbose_name=_('License Id'),
        max_length=255,
        db_column="license_id",
        null=True,
        blank=True
    )
    license_id_file = models.ForeignKey(
        Media,
        verbose_name=_('License File'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)sLicenseFiles'
    )

    def __str__(self):
        return str(self.user) + "(" + str(self.organization_type) + ")"

    class Meta:
        verbose_name = "Employer Profile"
        verbose_name_plural = "Employer Profiles"
        db_table = "EmployerProfile"
