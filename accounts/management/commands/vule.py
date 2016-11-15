from django.core.management.base import BaseCommand, CommandError
from accounts.models import Carrier, CarrierUser
from django.contrib.auth.models import User
from django.templatetags.static import static

class Command(BaseCommand):
    help = 'Create Vule User'


    def handle(self, *args, **options):
        carrier = Carrier(name = "VULE S.A", color_id=6, image=static("images/bus06.png"))
        carrier.save()
        user = User.objects.create_user('vule', None, 'vule')
        user.save()
        carrieruser = CarrierUser(user = user, carrier = carrier)
        carrieruser.save()
        print("Usuario Vule creado")