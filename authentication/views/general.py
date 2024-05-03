from authentication.mixins.admin import SuperuserAccessMixin
from authentication.views import UserList, CreateUser, UpdateUser


class AdminUserList(SuperuserAccessMixin, UserList):
    """ Subclass of UserList with access only to admin users """


class AdminCreateUser(SuperuserAccessMixin, CreateUser):
    """ Subclass of CreateUser with access only to admin users """


class AdminUpdateUser(SuperuserAccessMixin, UpdateUser):
    """ Subclass of UpdateUser with access only to admin users """

