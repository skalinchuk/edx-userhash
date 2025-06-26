"""
edx_userhash Django application initialization.
"""

from django.apps import AppConfig
from edx_django_utils.plugins.constants import PluginSettings


class EdxUserhashConfig(AppConfig):
    """
    Configuration for the edx_userhash Django application.
    """

    name = 'edx_userhash'
    label = "userhash"
    verbose_name = "User Hash"

    plugin_app = {
        PluginSettings.CONFIG: {
            'lms.djangoapp': {
                'common': {PluginSettings.RELATIVE_PATH: 'settings.common'},
                'production': {PluginSettings.RELATIVE_PATH: 'settings.production'},
            },
        },
    }

    def ready(self):
        from . import signals  # noqa: F401
        from . import admin # noqa: F401
