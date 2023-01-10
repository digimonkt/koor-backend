from django.db import models
from django.utils.translation import gettext as _
from model_utils.models import (
    SoftDeletableModel, UUIDModel, TimeStampedModel
)

from model_utils import (
    FieldTracker,
)
from typing import Optional, Iterable
import logging

from .exceptions import UserNotPassed

# Model Mixin

class BaseModel(
        UUIDModel,
        SoftDeletableModel,
        TimeStampedModel
    ):
    """
    An abstract base class model that provides self updating, fields.
    
    This model has:
        - models_utils.UUIDModel that ``id`` field on any model that inherits from it which will be the primary key.  
        - models_utils.SoftDeletableModel has a field ``is_removed`` which is set to True instead of removing the instance.  
        - models_utils.UserStampedModel that provides self updating ``created_by`` and ``updated_by`` fields.
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