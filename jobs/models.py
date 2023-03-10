from django.db import models
from django.utils.translation import gettext as _

from random import randint

from core.models import (
    SlugBaseModel, BaseModel, SoftDeleteModel
)
from users.models import (
    TimeStampedModel, User
)
from project_meta.models import (
    EducationLevel, Country, City, Language, Skill, Media
)

class JobCategory(SlugBaseModel, TimeStampedModel, models.Model):
    """
    This table is used to store details about a Job Category.

    Columns: 
    - `title`: A string representing the name of the tag. 
    - `slug`: A string representing the slug for the tag, used in URLs or filtering process.
    """
    class Meta:
        verbose_name = "Job Category"
        verbose_name_plural = "Job Categories"
        db_table = "JobCategory"
        ordering = ['title']

class JobDetails(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    This is a Django model for a Job object, with the following fields:

    - `user`: the user associated with the job
    - `title`: the title of the job
    - `budget_currency`: the currency used for the job budget
    - `budget_amount`: the amount of the job budget
    - `budget_pay_period`: the pay period associated with the job budget
    - `description`: a description of the job
    - `country`: the country where the job is located
    - `city`: the city where the job is located
    - `address`: the address of the job
    - `job_category`: the category of the job
    - `is_full_time`: a Boolean indicating whether the job is full-time or not
    - `is_part_time`: a Boolean indicating whether the job is part-time or not
    - `has_contract`: a Boolean indicating whether the job has a contract or not
    - `contact_email`: the contact email for the job
    - `contact_phone`: the contact phone number for the job
    - `contact_whatsapp`: the contact Whatsapp number for the job
    - `highest_education`: the highest level of education required for the job
    - `language`: the language(s) required for the job
    - `skills`: the skill(s) required for the job
    - `status`: the status of the job
    """
    PAY_PERIOD_CHOICE = (
        ('yearly', "Yearly"),
        ('quarterly', "Quarterly"),
        ('monthly', "Monthly"),
        ('weekly', "Weekly"),
        ('hourly', "Hourly"),
    )
    WORKING_DAYS_CHOICE = [(str(i), str(i)) for i in range(1,8)]
    STATUS_CHOICE = (
        ('active', "Active"),
        ('inactive', "Inactive"),
        ('hold', "Hold"),
        ('deleted', "Deleted"),
        ('expired', "Expired"),
    )
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)s_user'
    )
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=255,
        db_column="title",
    )
    job_id = models.CharField(
        verbose_name=_('Job Id'),
        max_length=255,
        db_column="job_id",
        null=True,
        blank=True,
        unique=True
    )
    budget_currency = models.CharField(
        verbose_name=_('Budget Currency'),
        max_length=5,
        null=True,
        blank=True,
        db_column="budget_currency",
        default="KES"
    )
    budget_amount = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Budget Amount'),
        db_column="budget_amount",
    )
    budget_pay_period = models.CharField(
        verbose_name=_('Budget Pay Period'),
        db_column="budget_pay_period",
        max_length=255,
        null=True,
        blank=True,
        choices=PAY_PERIOD_CHOICE,
    )
    description = models.TextField(
        verbose_name=_('Description'),
        null=True,
        blank=True,
        db_column="description",
    )
    country = models.ForeignKey(
        Country,
        verbose_name=_('Country'),
        on_delete=models.CASCADE,
        db_column="country",
        related_name='%(app_label)s_%(class)s_country'
    )
    city = models.ForeignKey(
        City,
        verbose_name=_('City'),
        on_delete=models.CASCADE,
        db_column="city",
        related_name='%(app_label)s_%(class)s_city'
    )
    address = models.TextField(
        verbose_name=_('Address'),
        db_column="address",
    )
    job_category = models.ManyToManyField(
        to=JobCategory,
        verbose_name=_('Job Category'),
        db_column="job_category",
        related_name='%(app_label)s_%(class)s_job_category'
    )
    is_full_time = models.BooleanField(
        verbose_name=_('Is Full-time'),
        null=True,
        blank=True,
        db_column="is_full_time",
        default=False
    )
    is_part_time = models.BooleanField(
        verbose_name=_('Is Part-time'),
        null=True,
        blank=True,
        db_column="is_part_time",
        default=False
    )
    has_contract = models.BooleanField(
        verbose_name=_('Has Contract'),
        null=True,
        blank=True,
        db_column="has_contract",
        default=False
    )
    contact_email = models.EmailField(
        verbose_name=_('Contact Email'),
        null=True,
        blank=True,
        db_column="contact_email",
    )
    contact_phone = models.CharField(
        verbose_name=_('Contact Phone'),
        null=True,
        blank=True,
        max_length=15,
        db_column="contact_phone",
    )
    contact_whatsapp = models.CharField(
        verbose_name=_('Contact Whatsapp'),
        null=True,
        blank=True,
        max_length=15,
        db_column="contact_whatsapp",
    )
    highest_education = models.ForeignKey(
        to=EducationLevel,
        verbose_name=_('Highest Education'),
        on_delete=models.SET_NULL,
        db_column="highest_education",
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)s_highest_education'
    )
    skill = models.ManyToManyField(
        to=Skill,
        verbose_name=_('Skill'),
        db_column="skill",
        related_name='%(app_label)s_%(class)s_skill'
    )
    working_days = models.CharField(
        verbose_name=_('Working Days'),
        db_column="working_days",
        max_length=25,
        choices=WORKING_DAYS_CHOICE,
    )
    deadline = models.DateField(
        verbose_name=_('Deadline'),
        db_column='deadline'
    )
    start_date = models.DateField(
        verbose_name=_('Start Date'),
        db_column='start_date',
    )
    status = models.CharField(
        verbose_name=_('Status'),
        db_column="status",
        max_length=25,
        choices=STATUS_CHOICE,
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Job Detail"
        verbose_name_plural = "Job Details"
        db_table = "JobDetails"
        ordering = ['-created']
    
    def save(self, *args, **kwargs):
        if not self.job_id:
            self.job_id = unique_job_id()
        return super().save(*args, **kwargs)
    
def unique_job_id():
    job_id = str(randint(1000, 9999)) + "-" + str(randint(1000, 9999))
    try:
        if JobDetails.objects.get(job_id=job_id):
            return unique_job_id()
    except JobDetails.DoesNotExist:
        return job_id
    
class JobAttachmentsItem(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    This is a Django model for a Job Attachment object, associated with a specific Job item, with the following fields:

    - `job`: the job associated with the attachment
    - `attachment`: the attachment uploaded for the job
    """
    job = models.ForeignKey(
        JobDetails,
        verbose_name=_('Job'),
        on_delete=models.CASCADE,
        db_column="job",
        null=True,
        related_name='%(app_label)s_%(class)s_job'
    )
    attachment = models.OneToOneField(
        Media,
        verbose_name=_('Attachment'),
        on_delete=models.CASCADE,
        db_column="attachment",
        related_name='%(app_label)s_%(class)s_attachment'
    )

    def __str__(self):
        return str(self.job)

    class Meta:
        verbose_name = "Job Attachments Item"
        verbose_name_plural = "Job Attachments Items"
        db_table = "JobAttachmentsItem"
        ordering = ['-created']


class JobsLanguageProficiency(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    This Django model class represents the language proficiency of a job seeker. The fields are as follows:

    - `job`: The job in which this language proficiency belongs to.
    - `language`: The language of the language proficiency.
    - `written`: The written proficiency level of the language.
    - `spoken`: The spoken proficiency level of the language.
    """
    FLUENCY_CHOICE = (
        ('basic', "Basic"),
        ('conversational', "Conversational"),
        ('fluent', "Fluent"),
    )
    job = models.ForeignKey(
        JobDetails,
        verbose_name=_('Job'),
        on_delete=models.CASCADE,
        db_column="job",
        related_name='%(app_label)s_%(class)s_job'
    )
    language = models.ForeignKey(
        Language,
        verbose_name=_('Language'),
        on_delete=models.CASCADE,
        db_column="language",
        related_name='%(app_label)s_%(class)s_language'
    )
    written = models.CharField(
        verbose_name=_('Written'),
        max_length=255,
        db_column="written",
        choices=FLUENCY_CHOICE,
    )
    spoken = models.CharField(
        verbose_name=_('Spoken'),
        max_length=255,
        db_column="spoken",
        choices=FLUENCY_CHOICE,
    )

    def __str__(self):
        return str(self.language) + "(" + str(self.job) + ")"

    class Meta:
        verbose_name = "Jobs Language Proficiency"
        verbose_name_plural = "Jobs Language Proficiencies"
        db_table = "JobsLanguageProficiency"
        ordering = ['-created']
