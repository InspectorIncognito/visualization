from django.contrib.auth import backends
from models import ProxyUser


class ModelBackend(backends.ModelBackend):
    def get_user(self, user_id):
        try:
            return ProxyUser.objects.get(pk=user_id)
        except ProxyUser.DoesNotExist:
            return None

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = ProxyUser.objects.get(username = username)
            if user.check_password(password):
                return user
            else:
                return None
        except ProxyUser.DoesNotExist:
            return None
