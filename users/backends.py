from django.contrib.auth.backends import BaseBackend
from users.models import User
from django.db.models import Q

UserModel = User


# Custom Authentication Backend
class MobileOrEmailBackend(BaseBackend):
    """
    class MobileorEmailBackend is called by the django auth.
    Whenever we sign up or sign this class is invoke to
    authenticate the user.

    This class require two method implementation
    `authenticate` and `get_user`

    """

    def authenticate(self, identifier=None, password=None, role=None, **kwargs):
        try:

            # Try to fetch the user by searching the username or email field
            user = UserModel.objects.filter(role=role).get(Q(mobile_number=identifier) | Q(email=identifier))
            if user.check_password(password) and user.is_active:
                return user
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None