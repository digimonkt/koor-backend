from django.db import models
from django.utils.translation import gettext as _

from core.models import (
    BaseModel, SoftDeleteModel
)
from job.models import JobDetails
from project_meta.models import Media
from users.models import User, UserStampedModel


class SavedJob(BaseModel, SoftDeleteModel, UserStampedModel, models.Model):
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


class AppliedJob(BaseModel, SoftDeleteModel, UserStampedModel, models.Model):
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
    shortlisted_at = models.DateTimeField(
        verbose_name=_('Short Listed At'),
        null=True,
        blank=True,
        db_column="shortlisted_at"
    )
    rejected_at = models.DateTimeField(
        verbose_name=_('Rejected At'),
        null=True,
        blank=True,
        db_column="rejected_at"
    )
    resume = models.ForeignKey(
        Media,
        verbose_name=_('Resume'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="resume",
        related_name='%(app_label)s_%(class)s_resume'
    )

    def __str__(self):
        return str(self.job) + "(" + str(self.user) + ")"

    class Meta:
        verbose_name = "Applied Job"
        verbose_name_plural = "Applied Jobs"
        db_table = "AppliedJob"
