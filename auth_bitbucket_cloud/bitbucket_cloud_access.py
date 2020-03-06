"""
Backend that defers to Bitbucket Cloud for access control.
"""
import re
from pypicloud.access import IAccessBackend
from pyramid.request import Request
from auth_bitbucket_cloud.bitbucket import Bitbucket
from bitbucket.exceptions import AuthenticationUserAttributeError


class BitbucketCloudAccess(IAccessBackend):
    """
    This backend allows you to defer all user auth and permissions to the
    Bitbucket Cloud. It requires the ``requests`` package.
    """
    __auth_teams: dict
    __hashed_password: bool
    __ttl: int
    __cache: bool
    __default_email_domain: str
    __bitbucket: Bitbucket = None

    def __init__(
            self,
            request: Request = None,
            auth_teams: str = None,
            hashed_password: str = None,
            ttl: str = None,
            cache: str = None,
            default_email_domain: str = None
    ):
        super().__init__(request)
        self.__hashed_password = bool(hashed_password)
        self.__ttl = int(ttl)
        self.__auth_teams = BitbucketCloudAccess.__parse_allowed_teams(auth_teams)
        self.__cache = bool(cache)
        self.__default_email_domain = default_email_domain

    @classmethod
    def configure(cls, settings: dict) -> dict:
        """
        Configure the access backend with app settings.

        :param settings: dict Settings from ini file.
        :return: dict
        """
        return {
            'auth_teams': settings.get('auth.bitbucket.allow', ''),
            'hashed_password': settings.get('auth.bitbucket.hash_password', 'True'),
            'ttl': settings.get('auth.bitbucket.ttl', '300'),
            'cache': settings.get('auth.bitbucket.cache', 'False'),
            'default_email_domain': settings.get('auth.bitbucket.default_email_domain', '')
        }

    @staticmethod
    def __parse_allowed_teams(team_configuration: str) -> dict:
        allowed_teams: dict = {}
        team_pattern: any = re.compile(r'^(.*?)(\((.*?)\))?$')

        for team_permission in re.split(r'\s*,\s*', team_configuration):
            if team_pattern.match(team_permission):
                team: str = team_permission.split('(', 1)[0]
                permission: str = re.findall(r'\((.*?)\)', team_permission)[0] \
                    if '(' in team_permission else ''
                allowed_teams[team] = permission.split('|')

        return allowed_teams

    def allow_register(self) -> bool:
        """
        Check if the backend allows registration.
        This should only be overridden by mutable backends

        :return: bool
        """
        return False

    def allow_register_token(self) -> bool:
        """
        Check if the backend allows registration via tokens.
        This should only be overridden by mutable backends

        :return: bool
        """
        return False

    def _get_password_hash(self, username: str) -> str:
        """
        Get the stored password hash for a user.

        :param username: str The current user.
        :return: str
        """
        raise RuntimeError("Bitbucket Cloud should never call _get_password_hash")

    def in_any_group(self, username, groups):
        return False

    def groups(self, username=None):
        return self.__bitbucket.get_groups() if isinstance(self.__bitbucket, Bitbucket) else []

    def group_members(self, group):
        pass

    def is_admin(self, username: str) -> bool:
        return Bitbucket.is_admin(username)

    def group_permissions(self, package):
        pass

    def user_permissions(self, package: str) -> dict:
        pass

    def user_package_permissions(self, username):
        pass

    def group_package_permissions(self, group):
        pass

    def user_data(self, username: str = None) -> dict or list:
        """
        Get a list of all users or data for a single user.
        For Mutable backends, this MUST exclude all pending users.

        :param username: str The username to get data from.
        :return: dict
        """
        if username == self.__bitbucket.username or username is None:
            return self.__bitbucket.get_user_data() if username is not None else []
        else:
            raise AuthenticationUserAttributeError(
                'The given username does not match the logged in username.'
            )

    def verify_user(self, username: str, password: str) -> bool:
        """
        Check the login credentials of a user.

        :param username: str The login username.
        :param password: str The login password.
        :return: bool
        """
        # TODO: Hash password
        username = '@'.join([username, self.__default_email_domain]) \
            if len(self.__default_email_domain) > 0 else username
        self.__bitbucket = Bitbucket('basic', username, password)
        return self.__bitbucket.validate_credentials()
