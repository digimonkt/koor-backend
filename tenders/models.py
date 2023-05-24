from random import randint

from django.db import models
from django.utils.translation import gettext as _

from core.models import (
    SlugBaseModel, BaseModel, SoftDeleteModel
)
from project_meta.models import (
    Country, City, Media,
    Tag, Choice, OpportunityType
)
from users.models import (
    TimeStampedModel, User
)


class TenderCategory(SlugBaseModel, TimeStampedModel, models.Model):
    """
    This table is used to store details about a Tender Category.

    Columns: 
    - `title`: A string representing the name of the tag. 
    - `slug`: A string representing the slug for the tag, used in URLs or filtering process.
    """

    class Meta:
        verbose_name = "Tender Category"
        verbose_name_plural = "Tender Categories"
        db_table = "TenderCategory"
        ordering = ['title']


class TenderDetails(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    A Django model representing a tender detail, containing information such as the tender ID, budget, location,
    category, and sector.

    Attributes:
        - `SECTOR_CHOICE (tuple)`: A tuple of sector choices for the tender.
        - `user (ForeignKey)`: A foreign key representing the user who created the tender.
        - `title (CharField)`: A character field representing the title of the tender.
        - `tender_id (CharField)`: A character field representing the unique ID of the tender, generated by the
            `unique_tender_id()` function.
        - `budget_currency (CharField)`: A character field representing the currency of the budget.
        - `budget_amount (DecimalField)`: A decimal field representing the budget amount.
        - `description (TextField)`: A text field representing the description of the tender.
        - `country (ForeignKey)`: A foreign key representing the country where the tender is located.
        - `city (ForeignKey)`: A foreign key representing the city where the tender is located.
        - `tender_category (ManyToManyField)`: A many-to-many field representing the categories of the tender.

    Methods:
        - `__str__()`: Returns the string representation of the tender's title.
        - `save()`: Overrides the default `save()` method to generate a unique tender ID if one does not already exist.

    Meta:
        - `verbose_name (str)`: A string representing the singular name of the model.
        - `verbose_name_plural (str)`: A string representing the plural name of the model.
        - `db_table (str)`: A string representing the name of the database table for the model.
        - `ordering (list)`: A list representing the default sorting order for the model's objects.
    """

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
    tender_id = models.CharField(
        verbose_name=_('Tender Id'),
        max_length=255,
        db_column="tender_id",
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
    tag = models.ManyToManyField(
        to=Tag,
        verbose_name=_('Tag'),
        db_column="tag",
        related_name='%(app_label)s_%(class)s_tag'
    )
    tender_category = models.ManyToManyField(
        to=TenderCategory,
        verbose_name=_('Tender Category'),
        db_column="tender_category",
        related_name='%(app_label)s_%(class)s_tender_category'
    )
    tender_type = models.ManyToManyField(
        to=OpportunityType,
        verbose_name=_('Tender Type'),
        db_column="tender_type",
        related_name='%(app_label)s_%(class)s_tender_type'
    )
    sector = models.ManyToManyField(
        to=Choice,
        verbose_name=_('Sector'),
        db_column="sector",
        related_name='%(app_label)s_%(class)s_sectors'
    )
    deadline = models.DateField(
        verbose_name=_('Deadline'),
        db_column='deadline'
    )
    start_date = models.DateField(
        verbose_name=_('Start Date'),
        db_column='start_date',
        null=True,
        blank=True
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
        verbose_name = "Tender Detail"
        verbose_name_plural = "Tender Details"
        db_table = "TenderDetails"
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.tender_id:
            self.tender_id = unique_tender_id()
        return super().save(*args, **kwargs)


def unique_tender_id():
    """
    Generates a unique tender ID using two random numbers and checks if it already exists in the TenderDetails model.
    If the ID already exists, it recursively calls itself to generate a new unique ID.

    Returns:
        str: A unique tender ID in the format `"XXXX-XXXX"`, where X represents a digit between `0-9`.

    Raises:
        None
    """

    tender_id = str(randint(1000, 9999)) + "-" + str(randint(1000, 9999))
    try:
        if TenderDetails.objects.get(tender_id=tender_id):
            return unique_tender_id()
    except TenderDetails.DoesNotExist:
        return tender_id


class TenderAttachmentsItem(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    This is a Django model for a Tender Attachment object, associated with a specific Tender item, with the following
    fields:

        - `tender`: the tender associated with the attachment
        - `attachment`: the attachment uploaded for the tender

    """

    tender = models.ForeignKey(
        TenderDetails,
        verbose_name=_('Tender'),
        on_delete=models.CASCADE,
        db_column="tender",
        null=True,
        related_name='%(app_label)s_%(class)s_tenders'
    )
    attachment = models.OneToOneField(
        Media,
        verbose_name=_('Attachment'),
        on_delete=models.CASCADE,
        db_column="attachment",
        related_name='%(app_label)s_%(class)s_attachment'
    )

    def __str__(self):
        return str(self.tender)

    class Meta:
        verbose_name = "Tender Attachments Item"
        verbose_name_plural = "Tender Attachments Items"
        db_table = "TenderAttachmentsItem"
        ordering = ['-created']


class TenderFilter(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    A Django model that represents a filter for tender opportunities.

    Attributes:
        - `user (ForeignKey)`: The user associated with this filter.
        - `title (TextField)`: The title of this filter.
        - `country (ForeignKey)`: The country associated with this filter.
        - `city (ForeignKey)`: The city associated with this filter.
        - `opportunity_type (CharField)`: The type of tender opportunities this filter is interested in.
        - `sector (CharField)`: The sector this filter is interested in.
        - `deadline (DateField)`: The deadline by which the tender opportunities must be submitted.
        - `budget (DecimalField)`: The budget for the tender opportunities.
        - `tender_category (ManyToManyField)`: The categories of tender opportunities this filter is interested in.
        - `tag (ManyToManyField)`: The tags associated with this filter.
        - `is_notification (BooleanField)`: Whether this filter should send notifications for new tender opportunities.

    Meta:
        - `verbose_name (str)`: The human-readable name for this model in singular.
        - `verbose_name_plural (str)`: The human-readable name for this model in plural.
        - `db_table (str)`: The database table name for this model.
        - `ordering (list)`: The default ordering for this model.
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
    opportunity_type = models.ManyToManyField(
        to=OpportunityType,
        null=True,
        blank=True,
        verbose_name=_('Opportunity Type'),
        db_column="opportunity_type",
        related_name='%(app_label)s_%(class)s_opportunity_types'
    )
    sector = models.ManyToManyField(
        to=Choice,
        null=True,
        blank=True,
        verbose_name=_('Sector'),
        db_column="sector",
        related_name='%(app_label)s_%(class)s_sector'
    )
    deadline = models.DateField(
        verbose_name=_('Deadline'),
        db_column="deadline",
        null=True,
        blank=True
    )
    budget_min = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Budget Minimum'),
        db_column="budget_min"
    )
    budget_max = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Budget Maximum'),
        db_column="budget_max"
    )
    tender_category = models.ManyToManyField(
        to=TenderCategory,
        null=True,
        blank=True,
        verbose_name=_('Tender Category'),
        db_column="tender_category",
        related_name='%(app_label)s_%(class)s_tender_category'
    )
    tag = models.ManyToManyField(
        to=Tag,
        null=True,
        blank=True,
        verbose_name=_('Tag'),
        db_column="tag",
        related_name='%(app_label)s_%(class)s_tags'
    )
    is_notification = models.BooleanField(
        verbose_name=_('Is Notification'),
        null=True,
        blank=True,
        db_column="is_notification",
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Tender Filter"
        verbose_name_plural = "Tender Filters"
        db_table = "TenderFilter"
        ordering = ['-created']
