import random, string
from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import gettext as _
from django.template.defaultfilters import slugify
from django.contrib.postgres.fields import ArrayField

from random import randint
from jobs.models import JobDetails
from core.models import (
    BaseModel, SlugBaseModel, SoftDeleteModel, upload_directory_path
)

from users.models import (
    TimeStampedModel, User
)
from project_meta.models import Media


class InvoiceIcon(BaseModel, models.Model):
    TYPE_CHOICE = (
        ('x', "X"),
        ('youtube', "Youtube"),
        ('instagram', "Instagram"),
        ('linkedin', "Linkedin"),
        ('facebook', "Facebook"),
    )
    type = models.CharField(
        verbose_name=_('Type'),
        max_length=250,
        db_column="type",
        choices=TYPE_CHOICE
    )
    icon = models.FileField(
        verbose_name=_('Icon'),
        unique=True,
        upload_to=upload_directory_path,
        db_column="icon",
    )

    def __str__(self):
        return str(self.type)

    class Meta:
        verbose_name = "Invoice Icon"
        verbose_name_plural = "Invoice Icons"
        db_table = "InvoiceIcon"



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
    subtitle = models.CharField(
        verbose_name=_('Subtitle'),
        db_column="subtitle",
        null=True,
        blank=True,
        max_length=255
    )
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
    ROLE_TYPE_CHOICE = (
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

    class Meta:
        verbose_name = "Faq Category"
        verbose_name_plural = "Faq Categories"
        db_table = "FaqCategory"
        ordering = ['title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) + "-" + slugify(self.role)
        return super().save(*args, **kwargs)


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
    """
    Represents a category logo in the application.

    Attributes:
        logo (Media): The logo associated with the category.
        status (bool): The status of the category logo.

    Meta:
        verbose_name (str): The singular name for the category logo model.
        verbose_name_plural (str): The plural name for the category logo model.
        db_table (str): The name of the database table for the category logo model.
        ordering (list): The default ordering for category logos.

    """

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
        verbose_name = "Category Logo"
        verbose_name_plural = "Category Logos"
        db_table = "CategoryLogo"
        ordering = ['-created']


class Testimonial(SlugBaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    Testimonial Model represents a testimonial given by a client.

    Inherits from SlugBaseModel, SoftDeleteModel, TimeStampedModel, and models.Model.

    Attributes:
        client_name (CharField): The name of the client providing the testimonial.
        client_company (CharField): The company of the client providing the testimonial.
        client_position (CharField): The position of the client providing the testimonial.
        description (TextField): The description or content of the testimonial.
        image (OneToOneField): An optional image associated with the testimonial.
        status (BooleanField): The status of the testimonial (active or inactive).

    Meta:
        verbose_name (str): The singular name used for the model in the admin interface.
        verbose_name_plural (str): The plural name used for the model in the admin interface.
        db_table (str): The name of the database table used to store the model's data.
        ordering (list): The default ordering for querysets of this model.

    """

    client_name = models.CharField(
        verbose_name=_('Client Name'),
        max_length=255,
        db_column="client_name",
    )
    client_company = models.CharField(
        verbose_name=_('Client Company'),
        max_length=255,
        db_column="client_company",
    )
    client_position = models.CharField(
        verbose_name=_('Client Position'),
        max_length=255,
        db_column="client_position",
    )
    description = models.TextField(
        verbose_name=_('Description'),
        null=True,
        blank=True,
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
    status = models.BooleanField(
        verbose_name=_('Status'),
        db_column="status",
        null=True,
        blank=True,
        default=False
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
        db_table = "Testimonial"
        ordering = ['-created']


class NewsletterUser(BaseModel, TimeStampedModel, models.Model):
    """
    Represents a newsletter subscriber.

    Attributes:
        email (str): The email address of the subscriber.
        role (str): The role of the subscriber.
        status (bool): The status of the subscriber (True for active, False for inactive).

    Meta:
        verbose_name (str): The human-readable name of the model.
        verbose_name_plural (str): The plural version of the verbose_name.
        db_table (str): The name of the database table for the model.
        ordering (list): The default ordering for querysets of this model.

    Methods:
        __str__(): Returns a string representation of the newsletter user object.
    """

    email = models.EmailField(
        verbose_name=_('Email Address'),
        unique=True,
        db_column="email"
    )
    role = models.EmailField(
        verbose_name=_('Role'),
        null=True,
        blank=True,
        default='user',
        db_column="role"
    )
    status = models.BooleanField(
        verbose_name=_('Status'),
        db_column="status",
        null=True,
        blank=True,
        default=False
    )

    def __str__(self):
        return str(self.email)

    class Meta:
        verbose_name = "Newsletter User"
        verbose_name_plural = "Newsletter Users"
        db_table = "NewsletterUser"
        ordering = ['-created']


class PointDetection(BaseModel, models.Model):
    """
    Represents a point detection entry in the database.

    This model stores information about points earned by a user.

    Attributes:
        points (int): The number of points earned. Can be null or blank. Default value is 5.

    Methods:
        __str__(): Returns a string representation of the points.

    Meta:
        verbose_name (str): A human-readable name for the model class.
        verbose_name_plural (str): A human-readable plural name for the model class.
        db_table (str): The name of the database table associated with the model.
    """
    points = models.BigIntegerField(
        null=True,
        blank=True,
        default=5,
        verbose_name=_('Points'),
        db_column="points",
    )

    def __str__(self):
        """
        Returns a string representation of the points.

        Returns:
            str: The string representation of the points.
        """
        return str(self.points)

    class Meta:
        verbose_name = "Point Detection"
        verbose_name_plural = "Points Detection"
        db_table = "PointDetection"


class RechargeHistory(BaseModel, TimeStampedModel, models.Model):
    """
    Model to store recharge history information.

    This model represents the history of recharges made by users. It includes details such as the user who made the
    recharge, a note (optional), the points associated with the recharge, and the amount paid for the recharge.

    Attributes:
        user (ForeignKey): A foreign key to the User who made the recharge.
        note (CharField): A note related to the recharge (optional).
        points (BigIntegerField): The points associated with the recharge.
        amount (BigIntegerField): The amount paid for the recharge.

    Methods:
        __str__(): Returns a string representation of the recharge instance.

    Meta:
        verbose_name (str): Singular name for the model in human-readable format.
        verbose_name_plural (str): Plural name for the model in human-readable format.
        db_table (str): Name of the database table for this model.
    """
    PACKAGE_TYPE_CHOICE = (
        ('none', "None"),
        ('gold', "Gold"),
        ('silver', "Silver"),
        ('copper', "Copper"),
    )
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)s_user'
    )
    note = models.CharField(
        verbose_name=_('Note'),
        max_length=255,
        db_column="note",
        null=True,
        blank=True
    )
    points = models.BigIntegerField(
        null=True,
        blank=True,
        default=5,
        verbose_name=_('Points'),
        db_column="points",
    )
    package = models.CharField(
        verbose_name=_('Package'),
        max_length=250,
        db_column="package",
        default='none',
        null=True,
        blank=True,
        choices=PACKAGE_TYPE_CHOICE
    )
    amount = models.BigIntegerField(
        null=True,
        blank=True,
        default=0,
        verbose_name=_('Amount'),
        db_column="amount",
    )

    def __str__(self):
        """
        Returns a string representation of the points.

        Returns:
            str: The string representation of the points.
        """
        return str(self.user) + "(" + str(self.points) + ")"

    class Meta:
        verbose_name = "Recharge History"
        verbose_name_plural = "Recharge History"
        db_table = "RechargeHistory"


class Packages(BaseModel, TimeStampedModel, models.Model):
    """
    This is a Django model for a Job Attachment object, associated with a specific Job item, with the following fields:

    - `job`: the job associated with the attachment
    - `attachment`: the attachment uploaded for the job
    """
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=255,
        db_column="title",
    )
    benefit = ArrayField(
        models.CharField(
            verbose_name=_('Benefit'),
            max_length=450,
            null=True,
            blank=True,
            db_column="benefit",
        ),
        blank=True,
        null=True
    )
    price = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Price'),
        db_column="price",
    )
    credit = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name=_('Credit'),
        db_column="credit",
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Package"
        verbose_name_plural = "Packages"
        db_table = "Packages"
        ordering = ['created']


class Invoice(BaseModel, TimeStampedModel, models.Model):
    """
    Represents an invoice associated with a user, detailing transaction information.

    Attributes:
        user (User): The user associated with this invoice.
        invoice_id (str): The unique identifier for this invoice.
        start_date (datetime.date): The start date of the invoice period.
        end_date (datetime.date): The end date of the invoice period.
        comment (str): Additional comments or notes related to the invoice.
        points (int): The number of points associated with the invoice.
        total (int): The total amount before any discounts or deductions.
        discount (int): The discount amount applied to the invoice.
        grand_total (int): The final total after applying discounts.
        is_send (bool): Indicates whether the invoice has been sent.

    Methods:
        __str__():
            Returns a string representation of the invoice, including user and points.

    Meta:
        verbose_name (str): Singular name for the Invoice model.
        verbose_name_plural (str): Plural name for the Invoice model.
        db_table (str): Name of the database table for storing invoices.
    """

    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)s_user'
    )
    job = models.ForeignKey(
        JobDetails,
        verbose_name=_('Job'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="job",
        related_name='%(app_label)s_%(class)s_job'
    )
    invoice_id = models.CharField(
        verbose_name=_('Invoice Id'),
        max_length=255,
        db_column="invoice_id",
        null=True,
        blank=True
    )
    start_date = models.DateField(
        verbose_name=_('Start Date'),
        null=True,
        blank=True,
        db_column='start_date',
    )
    end_date = models.DateField(
        verbose_name=_('End Date'),
        null=True,
        blank=True,
        db_column='end_date',
    )
    points = models.BigIntegerField(
        null=True,
        blank=True,
        default=0,
        verbose_name=_('Points'),
        db_column="points",
    )
    total = models.BigIntegerField(
        null=True,
        blank=True,
        default=0,
        verbose_name=_('Total'),
        db_column="total",
    )
    discount = models.BigIntegerField(
        null=True,
        blank=True,
        default=0,
        verbose_name=_('Discount'),
        db_column="discount",
    )
    grand_total = models.BigIntegerField(
        null=True,
        blank=True,
        default=0,
        verbose_name=_('Grand Total'),
        db_column="grand_total",
    )
    is_send = models.BooleanField(
        verbose_name=_('Is Send'),
        db_column="is_send",
        null=True,
        blank=True,
        default=False
    )

    def __str__(self):
        """
        Returns a string representation of the points.

        Returns:
            str: The string representation of the points.
        """
        return str(self.user) + "(" + str(self.points) + ")"

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoice"
        db_table = "Invoice"


def random_number_generator(size=6, chars=string.digits):
    """
    Generate a random string composed of specified characters.

    This function generates a random string of specified size, composed of characters from the given 'chars' parameter.
    By default, it generates a random number string of size 6 composed of digits.

    Args:
        size (int, optional): The length of the random string to be generated. Defaults to 6.
        chars (str, optional): The pool of characters from which the random string is formed. Defaults to string.digits.

    Returns:
        str: A random string of the specified size composed of the provided characters.

    Example:
        >>> random_number_generator()
        '325819'
        >>> random_number_generator(8, 'ABCDEF')
        'BFAEDCDB'
    """

    return ''.join(random.choice(chars) for _ in range(size))


def invoice_id_generator(instance):
    """
    Generate a unique invoice ID for the given instance using a random number generator.

    This function generates a unique invoice ID for the provided instance by repeatedly generating random numbers until
    a unique ID is found within the corresponding model's database records. It prevents duplicate invoice IDs by
    checking for existing records with the generated ID.

    Args:
        instance: An instance of a Django model for which the invoice ID needs to be generated.

    Returns:
        str: A unique invoice ID for the provided instance.

    Note:
        This function assumes the existence of a random_number_generator function and a corresponding model with an
        'invoice_id' field, represented by user_instance.

    Example:
        # Assuming there's a model named 'Invoice' with an 'invoice_id' field
        new_invoice = Invoice(...)
        unique_invoice_id = invoice_id_generator(new_invoice)
    """

    invoice_id = random_number_generator()
    user_instance = instance.__class__
    qs_exists = user_instance.objects.filter(invoice_id=invoice_id).exists()
    if qs_exists:
        return invoice_id_generator(instance)
    return invoice_id


def pre_save_create_invoice_id(sender, instance, *args, **kwargs):
    """
    Automatically generates and assigns an invoice ID to the provided instance if it doesn't already have one.
    
    This function is intended to be connected to the 'pre_save' signal of the 'Invoice' model. It checks if the
    provided instance lacks an invoice ID, and if so, generates a new unique invoice ID using the
    'invoice_id_generator' function and assigns it to the instance.
    
    Parameters:
        sender (class): The class that sends the signal (typically the 'Invoice' model class).
        instance: The instance being saved (an instance of the 'Invoice' model).
        *args: Additional positional arguments for the signal (not used in this function).
        **kwargs: Additional keyword arguments for the signal (not used in this function).
        
    Returns:
        None
        
    Example:
        pre_save.connect(pre_save_create_invoice_id, sender=Invoice)
        
    Note:
        The 'invoice_id_generator' function used in this function should be defined elsewhere and provide a
        mechanism to generate unique invoice IDs.
    """

    if not instance.invoice_id:
        instance.invoice_id = invoice_id_generator(instance)


pre_save.connect(pre_save_create_invoice_id, sender=Invoice)


class GoogleAddSenseCode(BaseModel, TimeStampedModel, models.Model):
    page_title = models.CharField(
        verbose_name=_('Page Title'),
        max_length=255,
        db_column="page_title",
    )
    code = models.TextField(
        verbose_name=_('Code'),
        db_column="code",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.code

    class Meta:
        verbose_name_plural = "Google Add Sense Code"


class UserRights(SlugBaseModel, TimeStampedModel, models.Model):
    rights_value = models.CharField(
        verbose_name=_('Rights Value'),
        max_length=255,
        db_column="rights_value",
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = "User Rights"
        verbose_name_plural = "User Rights"
        db_table = "UserRights"
        ordering = ['title']


class UserSubRights(SlugBaseModel, TimeStampedModel, models.Model):
    subrights_value = models.CharField(
        verbose_name=_('Subrights Value'),
        max_length=255,
        db_column="subrights_value",
        null=True,
        blank=True
    )
    rights = models.ForeignKey(
        UserRights,
        verbose_name=_('Rights'),
        on_delete=models.CASCADE,
        db_column="rights",
        related_name='%(app_label)s_%(class)s_rights'
    )
    
    class Meta:
        verbose_name = "User Sub Rights"
        verbose_name_plural = "User Sub Rights"
        db_table = "UserSubRights"
        ordering = ['title']
        
    def save(self, *args, **kwargs):
        if not self.slug or self.title != self._original_title:
            base_slug = slugify(self.title) + "-" + slugify(self.rights.title)
            unique_slug = base_slug
            counter = 1
            while UserSubRights.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        return super().save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_title = self.title


class Rights(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):

    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)s_user'
    )
    rights = models.ForeignKey(
        UserSubRights,
        verbose_name=_('Rights'),
        on_delete=models.CASCADE,
        db_column="rights",
        related_name='%(app_label)s_%(class)s_rights'
    )

    def __str__(self):
        return str(self.rights) + "(" + str(self.user) + ")"

    class Meta:
        verbose_name = "Rights"
        verbose_name_plural = "Rights"
        db_table = "Rights"
        ordering = ['-created']

