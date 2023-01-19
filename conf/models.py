from django.db import models
from django.utils.translation import gettext as _

from core.models import (
    BaseModel, SoftDeleteModel
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

    def __str__(self):
        return str(self.smtp_host)

    class Meta:
        verbose_name = "SMTP Setting"
        verbose_name_plural = "SMTP Settings"
        db_table = "SMTPSetting"
