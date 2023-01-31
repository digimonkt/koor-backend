from django.db import models
from django.utils.translation import gettext as _

from autoslug import AutoSlugField

from core.models import (
    BaseModel, upload_directory_path, SoftDeleteModel
)


class Media(BaseModel, models.Model):
    """
        This class created for get media detail.
        Here we have some useful field like:- file_path, media_type.
            - file_path is the path of local storage where file are store.
            - media_type show the file's type like Image, Video, Document.
    """
    MEDIA_TYPE_CHOICE = (
        ('image', "Image"),
        ('video', "Video"),
        ('document', "Document"),
    )
    file_path = models.FileField(
        verbose_name=_('File Path'),
        unique=True,
        upload_to=upload_directory_path,
        db_column="file_path",
    )
    media_type = models.CharField(
        verbose_name=_('Media Type'),
        max_length=250,
        db_column="media_type",
        choices=MEDIA_TYPE_CHOICE,
        default='image'
    )

    def __str__(self):
        return str(self.file_path)

    class Meta:
        verbose_name = "Media"
        verbose_name_plural = "Media"
        db_table = "Media"


class Tag(BaseModel, SoftDeleteModel, models.Model):
    """
    This class created for get tag detail.
    Here we have some useful field like:- title, slug.
        - title is the tag name field.
        - slug is used in url link for particular category.
    """
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
        return self.title

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        db_table = "Tag"


class Language(BaseModel, SoftDeleteModel, models.Model):
    """
    This class created for get language detail.
    Here we have some useful field like:- title, slug.
        - title is the language name field.
        - slug is used in url link for particular category.
    """
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
        return self.title

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"
        db_table = "Language"


class Skill(BaseModel, SoftDeleteModel, models.Model):
    """
    This class created for get skill detail.
    Here we have some useful field like:- title, slug.
        - title is the skill name field.
        - slug is used in url link for particular category.
    """
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
        return self.title

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
        db_table = "Skill"


class Country(BaseModel, SoftDeleteModel, models.Model):
    """
        This class created for get country detail.
        Here we have some useful field like:- title, slug, currency_code, country_code, iso_code2, iso_code3.
    """
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
    currency_code = models.CharField(
        verbose_name=_('Currency Code'),
        max_length=5,
        db_column="currency_code",
    )
    country_code = models.CharField(
        verbose_name=_('Country Code'),
        max_length=5,
        db_column="country_code",
    )
    iso_code2 = models.CharField(
        verbose_name=_('ISO Code 2'),
        max_length=10,
        db_column="iso_code2",
    )
    iso_code3 = models.CharField(
        verbose_name=_('ISO Code 3'),
        max_length=10,
        db_column="iso_code3",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        db_table = "Country"


class City(BaseModel, SoftDeleteModel, models.Model):
    """
            This class created for get country detail.
            Here we have some useful field like:- title, slug, country.
                - country is used as a reference key field of Country table.
    """
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
    country = models.ForeignKey(
        Country,
        verbose_name=_('Country'),
        on_delete=models.CASCADE,
        db_column="country",
        related_name='%(app_label)s_%(class)s_country'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
        db_table = "City"


class EducationLevel(BaseModel, SoftDeleteModel, models.Model):
    """
    This class created for get education level detail.
    Here we have some useful field like:- title, slug.
        - title is the level name field.
        - slug is used in url link for particular education level.
    """
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
        return self.title

    class Meta:
        verbose_name = "Education Level"
        verbose_name_plural = "Education Levels"
        db_table = "EducationLevel"
