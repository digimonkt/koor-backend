from django.db import models
from django.utils.translation import gettext as _

from core.models import (
    BaseModel, SlugBaseModel,  SoftDeleteModel, upload_directory_path
)


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