from django.db import models
from django.utils.translation import gettext as _

from core.models import (
    SlugBaseModel
)
from users.models import TimeStampedModel


class JobCategory(SlugBaseModel, TimeStampedModel, models.Model):
    """
    This table is used to store details about a Job Category.

    Columns: 
    - `title`: A string representing the name of the tag. 
    - `slug`: A string representing the slug for the tag, used in URLs or filtering process.
    """
    class Meta:
        verbose_name = "Job Category"
        verbose_name_plural = "Job Categories"
        db_table = "JobCategory"
