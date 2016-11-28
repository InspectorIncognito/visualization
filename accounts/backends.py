from django.contrib.auth import backends
from models import ProxyUser


class ModelBackend(backends.ModelBackend):
    def get_user(self, user_id):
        try:
            return ProxyUser.objects.get(pk=user_id)
        except ProxyUser.DoesNotExist:
            return None