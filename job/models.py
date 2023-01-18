from autoslug import AutoSlugField
from django.db import models
from django.utils.translation import gettext as _

from core.models import (
    BaseModel, SoftDeleteModel
)


class JobCategory(BaseModel, SoftDeleteModel, models.Model):
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
        return str(self.title)

    class Meta:
        verbose_name = "Job Category"
        verbose_name_plural = "Job Categories"
        db_table = "JobCategory"
