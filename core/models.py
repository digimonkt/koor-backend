from datetime import date
import time
from django.db import models
from django.utils.translation import gettext as _
from django.template.defaultfilters import slugify

from model_utils import (
    FieldTracker,
)
from model_utils.models import (
    UUIDModel, SoftDeletableModel
)


# Model Mixin

def upload_directory_path(instance, filename):
    """
    Directory path function: Return unique path name for file uploading.
    Example:- YYYT-MM-DD/instance_name/file_name
    """
    return '{0}/{1}/{2}'.format(date.today(), (str(instance).split('.')[0]) + "_" + str(time.time()).split('.')[0], filename)

class BaseModel(UUIDModel):
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
    """
    Soft Delete Model Class: This is an abstract class model use for SoftDeletableModel and active field into model
    class.
    SoftDeleteModel : - with the help of this function we remove record partially, and we easily store this
    partially removed record into table.
    """
    active = models.BooleanField(
        verbose_name=_('Active'),
        default=True,
        blank=True,
        null=True,
        db_column="active"
    )

    class Meta:
        abstract = True

class SlugBaseModel(BaseModel, SoftDeleteModel, models.Model):
    """ 
    This abstract base model is used to store information in a Django Model.

    Columns: 
    - `title`: A string representing the name of the model. 
    - `slug`: A string representing the slug for the model, used in URLs and filtering record.
    """
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=255,
        db_column="title",
    )
    slug = models.SlugField(
        unique=True,
        max_length=455,
        null=True,
        blank=True,
        db_column="slug",
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True
