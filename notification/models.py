from django.db import models
from django.utils.translation import gettext as _

from core.models import (
    BaseModel, SoftDeleteModel
)

from users.models import (
    TimeStampedModel, User

)
from job_seekers.models import AppliedJob

from jobs.models import JobFilters, JobDetails


class Notification(BaseModel, SoftDeleteModel, TimeStampedModel, models.Model):
    """
    A model that represents a notification sent to a user.

    Attributes:
        - `user (ForeignKey)`: The user that the notification is intended for.
        - `notification_type (CharField)`: The type of the notification.
        - `application (ForeignKey)`: The applied job associated with the notification (if applicable).
        - `job_filter (ForeignKey)`: The job filter associated with the notification (if applicable).
        - `seen (BooleanField)`: Whether the notification has been seen by the user.

    Methods:
        __str__(): Returns a string representation of the notification.

    Meta:
        - `verbose_name (str)`: The singular name for the model.
        - `verbose_name_plural (str)`: The plural name for the model.
        - `db_table (str)`: The name of the database table to use for the model.
        - `ordering (list)`: The default ordering for the model.
    """

    NOTIFICATION_TYPE_CHOICE = (
        ('applied', "Applied"),
        ('password_update', "Password Updated"),
        ('shortlisted', "Shortlisted"),
        ('planned_interviews', "Planned Interviews"),
        ('message', "Message"),
        ('advance_filter', "Advance Filter"),
        ('expired_save_job', "Expired Save Job"),
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
    job = models.ForeignKey(
        JobDetails,
        verbose_name=_('Job'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="job",
        related_name='%(app_label)s_%(class)s_jobs'
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
