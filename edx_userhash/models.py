"""
Database models for edx_userhash.
"""
from django.db import models
from django.conf import settings
from model_utils.models import TimeStampedModel


class UserHash(TimeStampedModel):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="userhash"
    )
    hash = models.CharField(max_length=12, unique=True, db_index=True)

    class Meta:
        db_table = "userhash"

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        return '<UserHash, User ID: {}>'.format(self.pk)
