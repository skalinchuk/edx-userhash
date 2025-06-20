"""
edx_userhash Django application initialization.
"""

from django.apps import AppConfig


class OpenedxUserhashConfig(AppConfig):
    """
    Configuration for the edx_userhash Django application.
    """

    name = 'edx_userhash'
    label = "userhash"
    verbose_name = "User Hash"

    def ready(self):
        from . import signals  # noqa: F401
        from . import admin # noqa: F401
