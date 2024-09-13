from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models, migrations
from django.db.models.indexes import Index
from django.db.migrations import AddIndex

# Create your models here.

"""
This is an Action model used to store user activities.
"""
class Action(models.Model):
    user = models.ForeignKey( # the user who performs the actions
        settings.AUTH_USER_MODEL,
        related_name='actions',
        on_delete=models.CASCADE
    )
    verb = models.CharField(max_length=255) # the action that the user performs
    created = models.DateTimeField(auto_now_add=True) # date and time when this action was created; auto - when the action was first saved to the database
    target_ct = models.ForeignKey( # A ForeignKey field that points to the ContentType model
        ContentType,
        blank=True,
        null=True,
        related_name='target_obj',
        on_delete=models.CASCADE
    )
    target_id = models.PositiveIntegerField(null=True, blank=True) # a field for storing the primary key of the related object
    target = GenericForeignKey('target_ct', 'target_id') # a generic foreign key field to the related object based on the combination of the two previous fields
    """
    Class Meta defines a database index in descending order for the field 'created'
    """
    class Meta:
        indexes = [
            models.Index(fields=['created']),
            models.Index(fields=['target_ct', 'target_id']),
        ]
        ordering = ['-created']