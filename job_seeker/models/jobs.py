from django.db import models
from django.utils.translation import gettext as _

from core.models import (
    BaseModel, SoftDeleteModel
)
from job.models import JobDetails
from users.models import User


class SavedJob(BaseModel, SoftDeleteModel, models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)s_user'
    )
    job = models.ForeignKey(
        JobDetails,
        verbose_name=_('Job'),
        on_delete=models.CASCADE,
        db_column="job",
        related_name='%(app_label)s_%(class)s_job'
    )

    def __str__(self):
        return str(self.job) + "(" + str(self.user) + ")"

    class Meta:
        verbose_name = "Saved Job"
        verbose_name_plural = "Saved Jobs"
        db_table = "SavedJob"
