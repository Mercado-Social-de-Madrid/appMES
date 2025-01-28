from authentication.mixins.admin import SuperuserAccessMixin
from authentication.models.preregister import PreRegisteredUser
from authentication.views import UserList, CreateUser, UpdateUser


class AdminUserList(SuperuserAccessMixin, UserList):
    """ Subclass of UserList with access only to admin users """


class AdminCreateUser(SuperuserAccessMixin, CreateUser):
    """ Subclass of CreateUser with access only to admin users """

    def form_valid(self, form):
        response = super().form_valid(form)
        # Creating the preregistered user sends the welcome email
        PreRegisteredUser.objects.create(user=self.object)
        return response

class AdminUpdateUser(SuperuserAccessMixin, UpdateUser):
    """ Subclass of UpdateUser with access only to admin users """

