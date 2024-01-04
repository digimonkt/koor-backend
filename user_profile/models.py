from django.db import models
from django.utils.translation import gettext as _
from django.core.validators import RegexValidator

from core.models import (
    BaseModel, SoftDeleteModel
)

from users.models import User, TimeStampedModel
from project_meta.models import (
    EducationLevel, Media, Country,
    City, Choice, Tag
)

from jobs.models import JobCategory, JobSubCategory


class JobSeekerProfile(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    This model is used to store profile details of JobSeekers.

    Columns:

    - `user`: A User object representing the user.
    - `gender`: A string representing the user's gender.
    - `dob`: A date object representing the user's date of birth.
    - `employment_status`: A string representing the user's current employment status.
    - `description`: A string containing a description of the user.
    - `highest_education`: A  foreign key refrence to `project_meta.models.EducationLevel` representing the user's
        highest educational qualification.
    - `market_information_notification`: A boolean value indicating whether the user has opted to receive market
        information notifications.
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
    profile_title = models.CharField(
        verbose_name=_('Profile Title'),
        max_length=255,
        db_column="profile_title",
        null=True,
        blank=True
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
    experience = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Experience'),
        db_column="experience",
    )
    
    job_title = models.CharField(
        verbose_name=_('Job Title'),
        max_length=255,
        db_column="job_title",
        null=True,
        blank=True
    )
    short_summary = models.TextField(
        verbose_name=_('Short Summary'),
        null=True,
        blank=True,
        db_column="short_summary",
    )
    home_address = models.TextField(
        verbose_name=_('Home Address'),
        null=True,
        blank=True,
        db_column="home_address",
    )
    personal_website = models.TextField(
        verbose_name=_('Personal Website'),
        null=True,
        blank=True,
        db_column="personal_website",
    )
    

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Job Seeker Profile"
        verbose_name_plural = "Job Seeker Profiles"
        db_table = "JobSeekerProfile"
        ordering = ['created']


class Reference(models.Model):

    user = models.OneToOneField(
        to=User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)s_user'
    )
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
        db_column="country_code",
        validators=[
            RegexValidator(
                regex='^\+[1-9]\d{0,2}$',
                message='Invalid country code',
            ),
        ]
    )
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=250,
        blank=True,
        null=True,
        db_column="name"
    )

    class Meta:
        verbose_name = "Reference"
        verbose_name_plural = "References"
        db_table = "Reference"
        

class EmployerProfile(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    This model is used to store profile details of Employers.

    Columns:

    - `user`: A User object representing the user.
    - `description`: A string containing a description of the user.
    - `organization_type`: A string representing the organization type the user is affiliated with.
    - `market_information_notification`: A boolean value indicating whether the user has opted to receive market
        information notifications.
    - `other_notification`: A boolean value indicating whether the user has opted to receive other information
        notifications.
    - `license_id`: A string representing the user's license ID.
    - `license_id_file`: A Media object representing the user's license ID file.
    """
    user = models.OneToOneField(
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
    address = models.TextField(
        verbose_name=_('Address'),
        null=True,
        blank=True,
        db_column="address",
    )
    website = models.URLField(
        verbose_name=_('Web Site'),
        null=True,
        blank=True,
        db_column="website",
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
    organization_type = models.ManyToManyField(
        to=Choice,
        verbose_name=_('Organization Type'),
        db_column="organization_type",
        related_name='%(app_label)s_%(class)s_organization_types'
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
    is_verified = models.BooleanField(
        verbose_name=_('Is Verified'),
        null=True,
        blank=True,
        default=False,
        db_column="is_verified",
    )
    points = models.BigIntegerField(
        null=True,
        blank=True,
        default=500,
        verbose_name=_('Points'),
        db_column="points",
    )

    def __str__(self):
        return str(self.user) + "(" + str(self.user.email) + ")"

    class Meta:
        verbose_name = "Employer Profile"
        verbose_name_plural = "Employer Profiles"
        db_table = "EmployerProfile"
        ordering = ['created']


class VendorProfile(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    Model representing the profile of a vendor in the system.

    Attributes:
        - `user (django.db.models.OneToOneField)`: One-to-one relationship with the User model representing the user
            associated with this vendor profile.
        - `description (django.db.models.TextField)`: A description of the vendor's organization.
        - `organization_type (django.db.models.CharField)`: The type of organization the vendor belongs to, chosen from
            a pre-defined list of choices.
        - `market_information_notification (django.db.models.BooleanField)`: A flag indicating whether the vendor wants
            to receive notifications about market information.
        - `other_notification (django.db.models.BooleanField)`: A flag indicating whether the vendor wants to receive
            other notifications.
        - `license_id (django.db.models.CharField)`: The ID of the vendor's license, if applicable.
        - `license_id_file (django.db.models.OneToOneField)`: A reference to the file containing the vendor's license,
            if applicable.
        - `registration_number (django.db.models.CharField)`: The registration number of the vendor's organization, if
            applicable.
        - `registration_certificate (django.db.models.OneToOneField)`: A reference to the file containing the vendor's
            registration certificate, if applicable.
        - `operating_years (django.db.models.BigIntegerField)`: The number of years the vendor's organization has been
            operating.
        - `jobs_experience (django.db.models.BigIntegerField)`: The number of years of job experience the vendor has.

    Methods:
        - `__str__(self)`: Returns a string representation of the VendorProfile object.

    Meta:
        - `verbose_name (str)`: A human-readable name for the model in singular form.
        - `verbose_name_plural (str)`: A human-readable name for the model in plural form.
        - `db_table (str)`: The name of the database table to use for the model.
        - `ordering (list)`: A list of fields to use for ordering the model instances.
    """
    user = models.OneToOneField(
        to=User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)s_users'
    )
    description = models.TextField(
        verbose_name=_('Description'),
        null=True,
        blank=True,
        db_column="description",
    )
    organization_type = models.ManyToManyField(
        to=Choice,
        verbose_name=_('Organization Type'),
        db_column="organization_type",
        related_name='%(app_label)s_%(class)s_organization_types'
    )
    website = models.URLField(
        verbose_name=_('Web Site'),
        null=True,
        blank=True,
        db_column="website",
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
    registration_number = models.CharField(
        verbose_name=_('Registration Number'),
        max_length=255,
        db_column="registration_number",
        null=True,
        blank=True
    )
    registration_certificate = models.OneToOneField(
        Media,
        verbose_name=_('Registration Certificate'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="registration_certificate",
        related_name='%(app_label)s_%(class)s_registration_certificates'
    )
    operating_years = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Operating Years'),
        db_column="operating_years",
    )
    jobs_experience = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Jobs Experience'),
        db_column="jobs_experience",
    )
    address = models.TextField(
        verbose_name=_('Address'),
        null=True,
        blank=True,
        db_column="address",
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
        return str(self.user) + "(" + str(self.organization_type) + ")"

    class Meta:
        verbose_name = "Vendor Profile"
        verbose_name_plural = "Vendor Profiles"
        db_table = "VendorProfile"
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
        - `is_notification (BooleanField)`: A boolean field indicating if the user filter should send notification for
            user postings.
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
    ROLE_TYPE_CHOICE = (
        ('admin', "Admin"),
        ('job_seeker', "Job Seeker"),
        ('employer', "Employer"),
        ('vendor', "Vendor"),
    )
    role = models.CharField(
        verbose_name=_('Role'),
        max_length=250,
        db_column="role",
        choices=ROLE_TYPE_CHOICE
    )
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
        to=JobCategory,
        null=True,
        blank=True,
        verbose_name=_('Category'),
        db_column="category",
        related_name='%(app_label)s_%(class)s_category'
    )
    sub_category = models.ManyToManyField(
        to=JobSubCategory,
        null=True,
        blank=True,
        verbose_name=_('Sub Category'),
        db_column="sub_category",
        related_name='%(app_label)s_%(class)s_sub_category'
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
    is_notification = models.BooleanField(
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
    experience = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Experience'),
        db_column="experience",
    )
    organization_type = models.ManyToManyField(
        to=Choice,
        null=True,
        blank=True,
        verbose_name=_('Organization Type'),
        db_column="organization_type",
        related_name='%(app_label)s_%(class)s_organization_types'
    )
    sector = models.ManyToManyField(
        to=Choice,
        null=True,
        blank=True,
        verbose_name=_('Sector'),
        db_column="sector",
        related_name='%(app_label)s_%(class)s_sector'
    )
    tag = models.ManyToManyField(
        to=Tag,
        verbose_name=_('Tag'),
        null=True,
        blank=True,
        db_column="tag",
        related_name='%(app_label)s_%(class)s_tag'
    )
    years_in_market = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Years in Market'),
        db_column="years_in_market",
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "User Filter"
        verbose_name_plural = "User Filters"
        db_table = "UserFilters"
        ordering = ['-created']

class UserAnalytic(BaseModel, models.Model):
    """
    Model representing user analytics.

    Attributes:
        user (ForeignKey): The user associated with the analytic.
        date (DateField): The date of the analytic.
        count (BigIntegerField): The count value for the analytic.

    Meta:
        verbose_name (str): The human-readable name for a single object of this model.
        verbose_name_plural (str): The human-readable name for multiple objects of this model.
        db_table (str): The database table name for this model.
    """
    
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)s_user'
    )
    date = models.DateField(
        verbose_name=_('Date'),
        blank=True,
        null=True,
        db_column='date'
    )
    count = models.BigIntegerField(
        null=True,
        blank=True,
        default=0,
        verbose_name=_('Count'),
        db_column="count",
    )
    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "User Analytic"
        verbose_name_plural = "User Analytics"
        db_table = "UserAnalytic"
