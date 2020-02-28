"""
Backend that defers to Bitbucket Cloud for access control.
"""
from pypicloud.access import IAccessBackend


class BitbucketCloudAccess(IAccessBackend):
    """
    This backend allows you to defer all user auth and permissions to the
    Bitbucket Cloud. It requires the ``requests`` package.
    """

    def __init__(self, **kwargs: any):
        super().__init__(**kwargs)

    def _get_password_hash(self, username):
        pass

    def groups(self, username=None):
        pass

    def group_members(self, group):
        pass

    def is_admin(self, username):
        pass

    def group_permissions(self, package):
        pass

    def user_permissions(self, package):
        pass

    def user_package_permissions(self, username):
        pass

    def group_package_permissions(self, group):
        pass

    def user_data(self, username=None):
        pass
