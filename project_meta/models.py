from django.db import models
from django.utils.translation import gettext as _

from core.models import BaseModel, upload_directory_path


class Media(BaseModel, models.Model):
    MEDIA_TYPE_CHOICE = (
        ('image', "Image"),
        ('video', "Video"),
        ('document', "Document"),
    )

    file_path = models.FileField(
        verbose_name=_('File Path'),
        upload_to=upload_directory_path,
        null=True,
        blank=True,
        db_column="file_path",
    )
    media_type = models.CharField(
        verbose_name=__('Media Type'),
        max_length=250,
        blank=True,
        null=True,
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
