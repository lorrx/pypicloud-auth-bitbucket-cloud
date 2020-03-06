"""
Bitbucket Cloud generic object abstraction as entry point for new authentication connections.
"""
from enum import IntEnum
from .auth.basic_auth import BasicAuth
from .exceptions import AuthenticationTypeNotImplementedError


class AuthenticationType(IntEnum):
    """
    Enum class for all supported authentication types.
    """
    basic = 1


class Bitbucket(object):
    """
    Bitbucket class definition
    """
    __authentication: BasicAuth or object
    __username: str
    __password: str

    def __init__(self, auth_type: str, username: str, password: str):
        self.__username = username
        self.__password = password

        if auth_type in AuthenticationType.__members__:
            self.__authentication_loader(AuthenticationType[auth_type])
        else:
            raise AuthenticationTypeNotImplementedError(
                'The selected auth type "{}" is not implemented.'.format(auth_type)
            )

    @property
    def username(self) -> str:
        return self.__username

    def __authentication_loader(self, auth_type: AuthenticationType) -> None:
        if auth_type == AuthenticationType.basic:
            self.__authentication = BasicAuth(self.__username, self.__password)

    def validate_credentials(self) -> bool:
        """
        Validates the user credentials by calling the user API endpoint.

        :return: bool
        """
        return self.__authentication.get_user().status_code == 200

    def get_user_data(self) -> dict:
        return {
            'username': self.__username,
            'admin': self.is_admin(),
            'groups': self.get_groups()
        }

    def get_groups(self) -> list:
        return []

    @staticmethod
    def is_admin(username: str) -> bool:
        return True

