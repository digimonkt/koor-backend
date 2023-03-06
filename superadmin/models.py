from django.db import models
from django.utils.translation import gettext as _

from core.models import (
    BaseModel, SoftDeleteModel, upload_directory_path
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


class UserRights(BaseModel, SoftDeleteModel, models.Model):
    description = models.TextField(
        verbose_name=_('Description'),
        db_column="description",
    )

    def __str__(self):
        return str(self.description)

    class Meta:
        verbose_name = "User Rights"
        verbose_name_plural = "User Rights"
        db_table = "UserRights"


class PrivacyPolicy(BaseModel, SoftDeleteModel, models.Model):
    description = models.TextField(
        verbose_name=_('Description'),
        db_column="description",
    )

    def __str__(self):
        return str(self.description)

    class Meta:
        verbose_name = "Privacy Policy"
        verbose_name_plural = "Privacy Policies"
        db_table = "PrivacyPolicy"
