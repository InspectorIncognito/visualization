from django.core.management.base import BaseCommand, CommandError
from accounts.models import Carrier, CarrierUser
from django.contrib.auth.models import User
from django.templatetags.static import static

class Command(BaseCommand):
    help = 'Create Metbus User'


    def handle(self, *args, **options):
        carrier = Carrier(name = "METBUS S.A", color_id=7, image=static("images/bus07.png"))
        carrier.save()
        user = User.objects.create_user('metbus', None, 'metbus')
        user.save()
        carrieruser = CarrierUser(user = user, carrier = carrier)
        carrieruser.save()
        print("Usuario Metbus creado")