from django.db import models
from django.utils.translation import gettext as _

from core.models import (
    BaseModel, SlugBaseModel, upload_directory_path,
)

# Create your models here.

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
        return self.file_path

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
