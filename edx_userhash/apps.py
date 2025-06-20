"""
edx_userhash Django application initialization.
"""

from django.apps import AppConfig
from django.conf import settings


class OpenedxUserhashConfig(AppConfig):
    """
    Configuration for the edx_userhash Django application.
    """

    name = 'edx_userhash'
    label = "userhash"
    verbose_name = "User Hash"

    def ready(self):
        # Late import to avoid side effects during migrations
        from . import signals  # noqa: F401
        from . import admin # noqa: F401

        # --- NEW: register context-processor ---
        cp = "edx_userhash.context_processors.user_hash"
        opts = settings.TEMPLATES[0]["OPTIONS"]
        if cp not in opts["context_processors"]:
            opts["context_processors"].append(cp)
