from django.db import models
from django.utils.translation import gettext as _

from model_utils import (
    FieldTracker,
)
from model_utils.models import (
    UUIDModel, TimeStampedModel, SoftDeletableModel
)


# Model Mixin

def upload_directory_path(instance, filename):
    return '{0}/{1}'.format(instance, filename)


class BaseModel(
    UUIDModel,
    TimeStampedModel
):
    """
    An abstract base class model that provides self updating, fields.

    This model has:
        - models_utils.UUIDModel that ``id`` field on any model that inherits from it which will be the primary key.
        - models_utils.FieldTracker that can be added to a model to track changes in model fields.

    Reference: https://django-model-utils.readthedocs.io/en/latest/

    Example:
    class Post(models.Model):
        title = models.CharField(max_length=100)
        tracker = FieldTracker()

    >>> a = Post.objects.create(title='First Post')
    >>> a.title = 'Welcome'
    >>> a.tracker.previous('title')
    u'First Post'
    >>> a.tracker.has_changed('title')
    True
    >>> a.tracker.has_changed('body')
    False
    """
    # A FieldTracker allows querying for field changes since a model instance was last saved.
    tracker = FieldTracker()

    class Meta:
        abstract = True


class SoftDeleteModel(SoftDeletableModel, models.Model):
    active = models.BooleanField(
        verbose_name=_('Active'),
        default=True,
        blank=True,
        null=True,
        db_column="active"
    )

    class Meta:
        abstract = True
