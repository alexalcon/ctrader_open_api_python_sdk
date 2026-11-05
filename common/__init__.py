"""
common -- Shared helpers for the sandbox scripts.

Anything two or more scripts need (credentials, endpoint selection,
small converters) lives here so each script stays focused on the one
Open API concept it is exploring.
"""

from common.config import Settings, load_settings

__all__ = ["Settings", "load_settings"]
