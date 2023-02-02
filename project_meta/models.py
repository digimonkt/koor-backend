from django.db import models
from django.utils.translation import gettext as _

from core.models import (
    BaseModel, upload_directory_path
)

# Create your models here.

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
        return self.file_path

    class Meta:
        verbose_name = "Media"
        verbose_name_plural = "Media"
        db_table = "Media"
