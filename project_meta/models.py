from django.db import models
from django.utils.translation import gettext as _
from django.template.defaultfilters import slugify

from core.models import (
    BaseModel, SlugBaseModel, upload_directory_path
)


class Media(BaseModel, models.Model):
    """ 
    This table stores information about media files uploaded to the system.

    Columns: 
    - `filepath`: A string representing the path of the media file. 
    - `mediatype`: A string representing the type of media (e.g. image, video, audio).

    Returns: models.Model. 
    """
    MEDIA_TYPE_CHOICE = (
        ('image', "Image"),
        ('video', "Video"),
        ('document', "Document"),
    )
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=250,
        db_column="title",
        null=True,
        blank=True
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


class Tag(SlugBaseModel, models.Model):
    """
    This table is used to store details about a tag.

    Columns: 
    - `title`: A string representing the name of the tag. 
    - `slug`: A string representing the slug for the tag, used in URLs or filtering process.
    """

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        db_table = "Tag"
        ordering = ['title']


class Language(SlugBaseModel, models.Model):
    """
    This table is used to store details about a language.

    Columns: 
    - `title`: A string representing the name of the language. 
    - `slug`: A string representing the slug for the language, used in URLs or filtering process.
    """

    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Langauges"
        db_table = "Language"
        ordering = ['title']


class Skill(SlugBaseModel, models.Model):
    """
    This table is used to store details about a skill.

    Columns: 
    - `title`: A string representing the name of the skill. 
    - `slug`: A string representing the slug for the skill, used in URLs or filtering process.
    """

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
        db_table = "Skill"
        ordering = ['title']


class EducationLevel(SlugBaseModel, models.Model):
    """
    This table is used to store details about a Education Level.

    Columns: 
    - `title`: A string representing the name of the education level. 
    - `slug`: A string representing the slug for the education level, used in URLs or filtering process.
    """

    class Meta:
        verbose_name = "Education Level"
        verbose_name_plural = "Education Levels"
        db_table = "EducationLevel"
        ordering = ['title']


class Country(SlugBaseModel, models.Model):
    """
    This table is used to store details about a Country.

    Columns: 
    - `title`: A string representing the name of the country. 
    - `slug`: A string representing the slug for the country, used in URLs or filtering process.
    - `iso_code2`: A string representing the two-letter ISO code for the country. 
    - `iso_code3`: A string representing the three-letter ISO code for the country. 
    - `currency_code`: A string representing the currency code for the country. 
    - `country_code`: A string representing the country code for the country.
    """
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

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        db_table = "Country"
        ordering = ['title']


class City(SlugBaseModel, models.Model):
    """
    This table is used to store details about a City.

    Columns: 
    - `title`: A string representing the name of the city. 
    - `slug`: A string representing the slug for the city, used in URLs or filtering process.
    - `country`: A foreign key reference to the country table.
    """

    country = models.ForeignKey(
        to=Country,
        verbose_name=_('Country'),
        on_delete=models.CASCADE,
        db_column="country",
        related_name='%(app_label)s_%(class)s_country'
    )

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
        db_table = "City"
        ordering = ['title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) + "-" + slugify(self.country)
        return super().save(*args, **kwargs)


class JobSeekerCategory(BaseModel, models.Model):
    """
    A model class representing the categories for job seekers.

    Attributes:
        - title (str): The title of the category.
        - category (ForeignKey): The parent category of this category.
        - Meta (class): A subclass of Model which defines the metadata for the model.

    """

    title = models.TextField(
        verbose_name=_('Title'),
        db_column="title",
    )
    category = models.ForeignKey(
        to='self',
        verbose_name=_('Category'),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_column="category",
        related_name='%(app_label)s_%(class)s_categories'
    )

    class Meta:
        verbose_name = "JobSeekerCategory"
        verbose_name_plural = "Job Seeker Categories"
        db_table = "JobSeekerCategory"
        ordering = ['title']
        """
        Metadata for the JobSeekerCategory model.
        - verbose_name (str): Human-readable name for the model in singular and plural form.
        - db_table (str): Database table name.
        - ordering (list): Default ordering for the model.

        """


class Sector(SlugBaseModel, models.Model):
    """
    This table is used to store details about a sector.

    Columns: 
    - `title`: A string representing the name of the sector. 
    - `slug`: A string representing the slug for the sector, used in URLs or filtering process.
    """

    class Meta:
        verbose_name = "Sector"
        verbose_name_plural = "Sectors"
        db_table = "Sector"
        ordering = ['title']


class AllCountry(models.Model):
    """
    This is the docstring for the AllCountry model class.

    AllCountry is a Django model representing country information including title, ISO codes, phone code,
    currency, and other details.

    Attributes:
        - title (CharField): Title of the country, with a maximum length of 150 characters.
        - iso3 (CharField): ISO Code 3 of the country, with a maximum length of 10 characters.
        - iso2 (CharField): ISO Code 2 of the country, with a maximum length of 10 characters.
        - phone_code (CharField): Phone code of the country, with a maximum length of 50 characters.
        - currency (CharField): Currency of the country, with a maximum length of 20 characters.
        
    Meta:
        - verbose_name (str): The singular name for the model, which is "All Country".
        - verbose_name_plural (str): The plural name for the model, which is "All Countries".
        - db_table (str): The name of the database table for the model, which is "AllCountry".
        - ordering (list): The default ordering for the model, which is based on the "title" attribute.

    """

    title = models.CharField(
        verbose_name=_('Title'),
        max_length=150,
        db_column="title",
    )
    iso3 = models.CharField(
        verbose_name=_('ISO Code 3'),
        max_length=10,
        db_column="iso3",
    )
    iso2 = models.CharField(
        verbose_name=_('ISO Code 2'),
        max_length=10,
        db_column="iso2",
    )
    phone_code = models.CharField(
        verbose_name=_('Phone Code'),
        max_length=50,
        db_column="phone_code",
    )
    currency = models.CharField(
        verbose_name=_('Currency'),
        max_length=20,
        db_column="currency",
    )

    class Meta:
        verbose_name = "All Country"
        verbose_name_plural = "All Countries"
        db_table = "AllCountry"
        ordering = ['title']


class AllCity(models.Model):
    """
    Model representing a city.

    Attributes:
        - `title (str)`: The name of the city.
        - `country (AllCountry)`: The country where the city is located.

    Meta:
        - `verbose_name (str)`: A human-readable name for the model in singular form.
        - `verbose_name_plural (str)`: A human-readable name for the model in plural form.
        - `db_table (str)`: The name of the database table to use for storing model data.
        - `ordering (list)`: The default ordering for the model's records.

    """

    title = models.CharField(
        verbose_name=_('Title'),
        max_length=150,
        db_column="title",
    )
    country = models.ForeignKey(
        to=AllCountry,
        verbose_name=_('Country'),
        on_delete=models.CASCADE,
        db_column="country",
        related_name='%(app_label)s_%(class)s_country'
    )
    
    class Meta:
        verbose_name = "All City"
        verbose_name_plural = "All Cities"
        db_table = "AllCity"
        ordering = ['title']
