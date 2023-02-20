from django.db import models
from django.utils.translation import gettext as _

from core.models import (
    BaseModel, SoftDeleteModel
)
from users.models import User, TimeStampedModel
from project_meta.models import (
    EducationLevel, Media
)

class JobSeekerProfile(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    This model is used to store profile details of JobSeekers.

    Columns:

    - `user`: A User object representing the user.
    - `gender`: A string representing the user's gender.
    - `dob`: A date object representing the user's date of birth.
    - `employment_status`: A string representing the user's current employment status.
    - `description`: A string containing a description of the user.
    - `highest_education`: A  foreign key refrence to `project_meta.models.EducationLevel` representing the user's highest educational qualification.
    - `market_information_notification`: A boolean value indicating whether the user has opted to receive market information notifications.
    - `job_notification`: A boolean value indicating whether the user has opted to receive job notifications.
    """
    GENDER_CHOICE = (
        ('male', "Male"),
        ('female', "Female"),
        ('trans', "Trans"),
    )
    EMPLOYMENT_STATUS_CHOICE = (
        ('employed', "Employed"),
        ('other', "Other"),
        ('fresher', "Fresher"),
    )
    user = models.OneToOneField(
        to=User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)s_user'
    )
    gender = models.CharField(
        verbose_name=_('Gender'),
        max_length=255,
        db_column="gender",
        choices=GENDER_CHOICE,
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
        db_column="highest_education",
        related_name='%(app_label)s_%(class)s_highest_educations'
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
        return str(self.user)

    class Meta:
        verbose_name = "Job Seeker Profile"
        verbose_name_plural = "Job Seeker Profiles"
        db_table = "JobSeekerProfile"

class EmployerProfile(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    This model is used to store profile details of Employers.

    Columns:

    - `user`: A User object representing the user.
    - `description`: A string containing a description of the user.
    - `organization_type`: A string representing the organization type the user is affiliated with.
    - `market_information_notification`: A boolean value indicating whether the user has opted to receive market information notifications.
    - `other_notification`: A boolean value indicating whether the user has opted to receive other information notifications.
    - `license_id`: A string representing the user's license ID.
    - `license_id_file`: A Media object representing the user's license ID file.
    """
    ORGANIZATION_TYPE_CHOICE = (
        ('government', "Government"),
        ('ngo', "NGO"),
        ('business', "Business"),
    )
    user = models.ForeignKey(
        to=User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)s_user'
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
    license_id_file = models.OneToOneField(
        Media,
        verbose_name=_('License File'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="license_id_file",
        related_name='%(app_label)s_%(class)s_license_files'
    )

    def __str__(self):
        return str(self.user) + "(" + str(self.organization_type) + ")"

    class Meta:
        verbose_name = "Employer Profile"
        verbose_name_plural = "Employer Profiles"
        db_table = "EmployerProfile"
