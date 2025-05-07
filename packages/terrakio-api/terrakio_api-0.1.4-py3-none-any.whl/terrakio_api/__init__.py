"""
Terrakio API Client

A Python client for accessing Terrakio's Web Coverage Service (WCS) API.
"""

__version__ = "0.1.0"

from .client import Client
from .config import create_default_config
from .exceptions import APIError, ConfigurationError, DownloadError, ValidationError

__all__ = [
    'Client',
    'create_default_config',
    'APIError',
    'ConfigurationError',
    'DownloadError',
    'ValidationError',
]