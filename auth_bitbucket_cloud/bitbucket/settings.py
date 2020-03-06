"""
Enum class for Bitbucket specific static settings.
"""
from enum import Enum


class Settings(Enum):
    """
    Settings class definition.
    """
    api_endpoint = 'https://api.bitbucket.org'
    api_version = '2.0'
