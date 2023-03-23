from django.db import models
from django.utils.translation import gettext as _

from core.models import (
    BaseModel, SoftDeleteModel
)

from users.models import (
    TimeStampedModel, User

)
from job_seekers.models import AppliedJob

from jobs.models import JobFilters

class Notification(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    NOTIFICATION_TYPE_CHOICE = (
        ('applied', "Applied"),
        ('password update', "Password Updated"),
        ('shortlisted', "Shortlisted"),
        ('message', "Message"),
        ('advance filter', "Advance Filter"),
    )
    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        on_delete=models.CASCADE,
        db_column="user",
        related_name='%(app_label)s_%(class)s_user'
    )
    notification_type = models.CharField(
        verbose_name=_('Notification Type'),
        db_column="nitification_type",
        max_length=25,
        choices=NOTIFICATION_TYPE_CHOICE,
    )
    application = models.ForeignKey(
        AppliedJob,
        verbose_name=_('Application'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="application",
        related_name='%(app_label)s_%(class)s_applications'
    )
    job_filter = models.ForeignKey(
        JobFilters,
        verbose_name=_('Job Filter'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="job_filter",
        related_name='%(app_label)s_%(class)s_job_filter'
    )
    seen = models.BooleanField(
        verbose_name=_('Seen'),
        null=True,
        blank=True,
        db_column="seen",
        default=False
    )
    
    def __str__(self):
        return str(self.notification_type) + '(' + str(self.user.id) + ')'
    
    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        db_table = "Notification"
        ordering = ['-created']
        