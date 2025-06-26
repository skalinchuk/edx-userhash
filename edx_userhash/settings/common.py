"""
Common settings required by the Userhash Plugin in context of LMS.
"""

from pathlib import Path


def plugin_settings(settings):
    """
    Override common settings.
    """
    settings.TEMPLATES[0]['OPTIONS']['context_processors'].append(
        'edx_userhash.context_processors.userhash_context'
    )
