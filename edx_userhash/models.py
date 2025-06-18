"""
Database models for edx_userhash.
"""
from django.db import models
from django.conf import settings
from model_utils.models import TimeStampedModel


class UserHash(TimeStampedModel):
    """
    TODO: replace with a brief description of the model.

    TODO: Add either a negative or a positive PII annotation to the end of this docstring.  For more
    information, see OEP-30:
    https://open-edx-proposals.readthedocs.io/en/latest/oep-0030-arch-pii-markup-and-auditing.html
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="userhash"
    )
    hash = models.CharField(max_length=64, unique=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "userhash"

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        return '<UserHash, User ID: {}>'.format(self.pk)
