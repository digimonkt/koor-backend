from autoslug import AutoSlugField
from django.db import models
from django.utils.translation import gettext as _

from core.models import (
    BaseModel, SoftDeleteModel
)
from project_meta.models import (
    Media, Language, Skill, Country, City, EducationLevel)
from users.models import User


class JobCategory(BaseModel, SoftDeleteModel, models.Model):
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=255,
        db_column="title",
    )
    slug = AutoSlugField(
        populate_from='title',
        always_update=True,
        unique=True,
        null=True,
        blank=True,
        db_column="slug",
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Job Category"
        verbose_name_plural = "Job Categories"
        db_table = "JobCategory"


class JobDetails(BaseModel, SoftDeleteModel, models.Model):
    PAY_PERIOD_CHOICE = (
        ('yearly', "Yearly"),
        ('quarterly', "Quarterly"),
        ('monthly', "Monthly"),
        ('weekly', "Weekly"),
        ('hourly', "Hourly"),
    )
    STATUS_CHOICE = (
        ('active', "Active"),
        ('inactive', "Inactive"),
        ('deleted', "Deleted"),
    )
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)sUser'
    )
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=255,
        db_column="title",
    )
    budget_currency = models.CharField(
        verbose_name=_('Budget Currency'),
        max_length=5,
        db_column="budget_currency",
        default="KES"
    )
    budget_amount = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        verbose_name=_('Budget Amount'),
        db_column="budget_amount",
    )
    budget_pay_period = models.CharField(
        verbose_name=_('Budget Pay Period'),
        db_column="budget_pay_period",
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
        related_name='%(app_label)s_%(class)sCountry'
    )
    city = models.ForeignKey(
        City,
        verbose_name=_('City'),
        on_delete=models.CASCADE,
        db_column="city",
        related_name='%(app_label)s_%(class)sCity'
    )
    address = models.TextField(
        verbose_name=_('Address'),
        db_column="address",
    )
    job_category_1 = models.ForeignKey(
        JobCategory,
        verbose_name=_('Job Category 1'),
        on_delete=models.CASCADE,
        db_column="job_category_1",
        related_name='%(app_label)s_%(class)sJobCategory1'
    )
    job_category_2 = models.ForeignKey(
        JobCategory,
        verbose_name=_('Job Category 2'),
        on_delete=models.SET_NULL,
        db_column="job_category_2",
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)sJobCategory2'
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
        EducationLevel,
        verbose_name=_('Highest Education'),
        on_delete=models.SET_NULL,
        db_column="highest_education",
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)sHighestEducation'
    )
    language_1 = models.ForeignKey(
        Language,
        verbose_name=_('Language 1'),
        on_delete=models.CASCADE,
        db_column="language_1",
        related_name='%(app_label)s_%(class)sLanguage1'
    )
    language_2 = models.ForeignKey(
        Language,
        verbose_name=_('Language 2'),
        on_delete=models.SET_NULL,
        db_column="language_2",
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)sLanguage2'
    )
    language_3 = models.ForeignKey(
        Language,
        verbose_name=_('Language 3'),
        on_delete=models.SET_NULL,
        db_column="language_3",
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)sLanguage3'
    )
    skill_1 = models.ForeignKey(
        Skill,
        verbose_name=_('Skill 1'),
        on_delete=models.CASCADE,
        db_column="skill_1",
        related_name='%(app_label)s_%(class)sSkill1'
    )
    skill_2 = models.ForeignKey(
        Skill,
        verbose_name=_('Skill 2'),
        on_delete=models.SET_NULL,
        db_column="skill_2",
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)sSkill2'
    )
    skill_3 = models.ForeignKey(
        Skill,
        verbose_name=_('Skill 3'),
        on_delete=models.SET_NULL,
        db_column="skill_3",
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)sSkill3'
    )
    status = models.CharField(
        verbose_name=_('Status'),
        db_column="status",
        null=True,
        blank=True,
        choices=STATUS_CHOICE,
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Job Detail"
        verbose_name_plural = "Job Details"
        db_table = "JobDetails"
