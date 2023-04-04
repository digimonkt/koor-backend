from django.db import models
from django.utils.translation import gettext as _

from core.models import (
    BaseModel, SoftDeleteModel
)

from users.models import User, TimeStampedModel
from project_meta.models import (
    EducationLevel, Media, Country, 
    City, JobSeekerCategory
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
    - `country (ForeignKey)`: A foreign key to the country associated with the job seeker profile.
    - `city (ForeignKey)`: A foreign key to the city associated with the job seeker profile.
    """
    GENDER_CHOICE = (
        ('male', "Male"),
        ('female', "Female"),
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
    country = models.ForeignKey(
        Country,
        verbose_name=_('Country'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        db_column="country",
        related_name='%(app_label)s_%(class)s_country'
    )
    city = models.ForeignKey(
        City,
        verbose_name=_('City'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        db_column="city",
        related_name='%(app_label)s_%(class)s_city'
    )

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Job Seeker Profile"
        verbose_name_plural = "Job Seeker Profiles"
        db_table = "JobSeekerProfile"
        ordering = ['created']

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
        ordering = ['created']


class UserFilters(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    Model representing a user filter created by a user to receive notifications about relevant User postings.

    Attributes:
        - `user (ForeignKey)`: A foreign key to the user who created the user filter.
        - `title (TextField)`: The title of the user filter.
        - `country (ForeignKey)`: A foreign key to the country associated with the user filter.
        - `city (ForeignKey)`: A foreign key to the city associated with the user filter.
        - `category (ManyToManyField)`: A many-to-many field to the categories associated with the user filter.
        - `is_full_time (BooleanField)`: A boolean field indicating if the user filter is for full-time users.
        - `is_part_time (BooleanField)`: A boolean field indicating if the user filter is for part-time users.
        - `is_notification (BooleanField)`: A boolean field indicating if the user filter should send notification for user postings.
        - `has_contract (BooleanField)`: A boolean field indicating if the user filter is for users with contracts.
        - `salary_min (CharField)`: A character field indicating the minimum salary for the user filter.
        - `salary_max (CharField)`: A character field indicating the maximum salary for the user filter.

   Methods:
       __str__(self): Returns a string representation of the user filter.

   Meta:
        - `verbose_name (str)`: The singular name for the model.
        - `verbose_name_plural (str)`: The plural name for the model.
        - `db_table (str)`: The name of the database table to use for the model.
        - `ordering (list)`: The default ordering for the model.
   """

    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)s_user'
    )
    title = models.TextField(
        verbose_name=_('Title'),
        db_column="title",
    )
    country = models.ForeignKey(
        Country,
        verbose_name=_('Country'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        db_column="country",
        related_name='%(app_label)s_%(class)s_country'
    )
    city = models.ForeignKey(
        City,
        verbose_name=_('City'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        db_column="city",
        related_name='%(app_label)s_%(class)s_city'
    )
    category = models.ManyToManyField(
        to=JobSeekerCategory,
        null=True,
        blank=True,
        verbose_name=_('Category'),
        db_column="category",
        related_name='%(app_label)s_%(class)s_category'
    )
    is_full_time = models.BooleanField(
        verbose_name=_('Is Full-time'),
        null=True,
        blank=True,
        db_column="is_full_time",
    )
    is_part_time = models.BooleanField(
        verbose_name=_('Is Part-time'),
        null=True,
        blank=True,
        db_column="is_part_time",
    )
    availability = models.BooleanField(
        verbose_name=_('Availability'),
        null=True,
        blank=True,
        db_column="availability",
    )
    is_notification= models.BooleanField(
        verbose_name=_('Is Notification'),
        null=True,
        blank=True,
        db_column="is_notification",
    )
    has_contract = models.BooleanField(
        verbose_name=_('Has Contract'),
        null=True,
        blank=True,
        db_column="has_contract",
    )
    salary_min = models.CharField(
        verbose_name=_('Salary Min'),
        max_length=250,
        blank=True,
        null=True,
        db_column="salary_min",
    )
    salary_max = models.CharField(
        verbose_name=_('Salary Max'),
        max_length=250,
        blank=True,
        null=True,
        db_column="salary_max",
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "User Filter"
        verbose_name_plural = "User Filters"
        db_table = "UserFilters"
        ordering = ['-created']
