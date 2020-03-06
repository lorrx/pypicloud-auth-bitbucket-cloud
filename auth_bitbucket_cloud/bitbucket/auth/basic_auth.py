"""
Bitbucket cloud basic auth implementation.

Basic HTTP Authentication as per RFC-2617 (Digest not supported). Note that
Basic Auth with username and password as credentials is only available on
accounts that have 2-factor-auth / 2-step-verification disabled. If you use
2fa, you should authenticate using OAuth2 instead.
"""
import requests
from bitbucket.settings import Settings


class BasicAuth(object):
    """
    Basic auth class definition.
    """
    __api_url: str
    __api_user: str
    __api_password: str

    def __init__(self, user: str, password: str):
        self.__api_user = user
        self.__api_password = password
        self.__api_url = '{}/{}'.format(
            Settings.api_endpoint.value,
            Settings.api_version.value
        )

    def get_user(self) -> requests.Response:
        return requests.get(
            '{}/user'.format(self.__api_url),
            auth=(self.__api_user, self.__api_password)
        )

    def get_teams(self, role: str) -> requests.Response:
        return requests.get(
            '{}/teams?role={}&pagelen=100'.format(self.__api_url, role),
            auth=(self.__api_user, self.__api_password)
        )
