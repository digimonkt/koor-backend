from django.db import models
from django.utils.translation import gettext as _
from django.contrib.postgres.fields import ArrayField

from core.models import (
    BaseModel, SlugBaseModel,  SoftDeleteModel, upload_directory_path
)

from users.models import (
    TimeStampedModel, User
)
from project_meta.models import Media

class SMTPSetting(BaseModel, SoftDeleteModel, models.Model):
    smtp_host = models.CharField(
        verbose_name=_('SMTP Host'),
        max_length=255,
        db_column="smtp_host",
    )
    smtp_user = models.CharField(
        verbose_name=_('SMTP User'),
        max_length=255,
        db_column="smtp_user",
    )
    smtp_port = models.CharField(
        verbose_name=_('SMTP Port'),
        max_length=255,
        db_column="smtp_port",
    )
    smtp_password = models.CharField(
        verbose_name=_('SMTP Password'),
        max_length=255,
        db_column="smtp_password",
    )
    logo = models.FileField(
        verbose_name=_('Logo'),
        unique=True,
        upload_to=upload_directory_path,
        db_column="logo",
    )

    def __str__(self):
        return str(self.smtp_host)

    class Meta:
        verbose_name = "SMTP Setting"
        verbose_name_plural = "SMTP Settings"
        db_table = "SMTPSetting"


class Content(SlugBaseModel, SoftDeleteModel, models.Model):
    description = models.TextField(
        verbose_name=_('Description'),
        db_column="description",
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Content"
        verbose_name_plural = "Contents"
        db_table = "Content"


class GooglePlaceApi(SoftDeleteModel, models.Model):
    api_key = models.CharField(
        verbose_name=_('API Key'),
        db_column="api_key",
        max_length=255
        )
    status = models.BooleanField(
        verbose_name=_('Status'),
        db_column="status",
        default=True
        )

    def __str__(self):
        return self.api_key
    
    class Meta:
        verbose_name_plural = "Google Place Api"

    
class ResourcesContent(SlugBaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    This is a Django model for a Job Attachment object, associated with a specific Job item, with the following fields:

    - `job`: the job associated with the attachment
    - `attachment`: the attachment uploaded for the job
    """
    description = ArrayField(
        models.TextField(
            verbose_name=_('Description'),
            null=True,
            blank=True,
            db_column="description",
        ),
        blank=True,
        null=True
    )
    attachment = models.OneToOneField(
        Media,
        verbose_name=_('Attachment'),
        on_delete=models.SET_NULL,
        db_column="attachment",
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)s_attachment'
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Resource"
        verbose_name_plural = "Resources"
        db_table = "Resources"
        ordering = ['-created']
    

class SocialUrl(BaseModel, SoftDeleteModel, models.Model):
    """
    Model representing a social URL.

    Fields:
        - platform (CharField): The platform of the social URL. Choices are predefined by PLATFORM_CHOICE.
        - url (URLField): The URL associated with the social platform.

    Methods:
        - __str__(): Returns a string representation of the platform.

    Meta:
        - verbose_name (str): Singular name for the model.
        - verbose_name_plural (str): Plural name for the model.
        - db_table (str): Name of the database table.
        - ordering (list): Default ordering for querysets.
    """
    
    PLATFORM_CHOICE = (
        ('iso_app', "ISO Application"),
        ('android_app', "Android Application"),
        ('facebook', "Facebook"),
        ('instagram', "Instagram"),
        ('linkedin', "Linkedin"),
        ('youtube', "Youtube"),
        ('twitter', "Twitter"),
    )
    platform = models.CharField(
        verbose_name=_('Platform'),
        max_length=255,
        db_column="platform",
        choices=PLATFORM_CHOICE,
    )
    url = models.URLField(
        verbose_name=_('Url'),
        db_column="url",
    )

    def __str__(self):
        return str(self.platform)

    class Meta:
        verbose_name = "Social Url"
        verbose_name_plural = "Social Urls"
        db_table = "SocialUrl"
        ordering = ['platform']


class AboutUs(SlugBaseModel, SoftDeleteModel, models.Model):
    """
    Model representing the 'About Us' section.

    Inherits from SlugBaseModel, SoftDeleteModel, and models.Model.

    Fields:
    - description (TextField): The description of the 'About Us' section.
    - image (OneToOneField[Media]): The image associated with the 'About Us' section.

    Meta:
    - verbose_name: The singular name of the model ('About Us').
    - verbose_name_plural: The plural name of the model ('About Us').
    - db_table: The database table name for the model ('AboutUs').

    Methods:
    - __str__(): Returns the string representation of the model instance (the title).

    """
    
    description = models.TextField(
        verbose_name=_('Description'),
        db_column="description",
    )
    image = models.OneToOneField(
        Media,
        verbose_name=_('Image'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        db_column="image",
        related_name='%(app_label)s_%(class)s_image'
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "About Us"
        verbose_name_plural = "About Us"
        db_table = "AboutUs"


class FaqCategory(SlugBaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    This table is used to store details about a FAQ Category.

    Columns: 
    - `title`: A string representing the name of the faq. 
    - `slug`: A string representing the slug for the faq, used in URLs or filtering process.
    """
    class Meta:
        verbose_name = "Faq Category"
        verbose_name_plural = "Faq Categories"
        db_table = "FaqCategory"
        ordering = ['title']


class FAQ(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    Represents a Frequently Asked Question (FAQ) in the system.

    Attributes:
        - user (ForeignKey): The user associated with the FAQ question.
        - question (CharField): The question being asked in the FAQ.
        - answer (TextField): The answer to the FAQ question.
        - category (ForeignKey): The category to which the FAQ question belongs.
        - status (BooleanField): The status of the FAQ question.
        - role (CharField): The role type associated with the FAQ question.

    Methods:
        - __str__(): Returns a string representation of the FAQ question.

    Meta:
        - verbose_name (str): The singular name for the FaqQuestion model.
        - verbose_name_plural (str): The plural name for the FaqQuestion model.
        - db_table (str): The database table name for the FaqQuestion model.
        - ordering (list): The default ordering for FaqQuestion objects.
    """

    ROLE_TYPE_CHOICE = (
        ('admin', "Admin"),
        ('job_seeker', "Job Seeker"),
        ('employer', "Employer"),
        ('vendor', "Vendor"),
    )
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)s_user'
    )
    question = models.CharField(
        verbose_name=_('Question'),
        max_length=255,
        db_column="question",
    )
    answer = models.TextField(
        verbose_name=_('Answer'),
        null=True,
        blank=True,
        db_column="answer",
    )
    category = models.ForeignKey(
        FaqCategory,
        verbose_name=_('Category'),
        on_delete=models.CASCADE,
        db_column="category",
        related_name='%(app_label)s_%(class)s_category'
    )
    status = models.BooleanField(
        verbose_name=_('Status'),
        db_column="status",
        default=True
    )
    role = models.CharField(
        verbose_name=_('Role'),
        max_length=250,
        db_column="role",
        choices=ROLE_TYPE_CHOICE
    )

    def __str__(self):
        return str(self.question)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        db_table = "FAQ"
        ordering = ['-created']


class CategoryLogo(BaseModel, TimeStampedModel, models.Model):

    logo = models.OneToOneField(
        Media,
        verbose_name=_('Logo'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        db_column="logo",
        related_name='%(app_label)s_%(class)s_logo'
    )
    status = models.BooleanField(
        verbose_name=_('Status'),
        db_column="status",
        null=True,
        blank=True,
        default=False
    )

    class Meta:
        verbose_name = "CategoryLogo"
        verbose_name_plural = "Category Logos"
        db_table = "CategoryLogo"
        ordering = ['-created']
