from django.core.management.base import BaseCommand
from accounts.models import Carrier
from django.templatetags.static import static

class Command(BaseCommand):
    help = 'Create Carriers'


    def handle(self, *args, **options):
        carrier = Carrier(name="Red Bus Urbano", color_id=1, image=static("carrier/images/bus02.png"))
        carrier.save()
        carrier = Carrier(name="Express", color_id=2, image=static("carrier/images/bus03.png"))
        carrier.save()
        carrier = Carrier(name="STP Santiago", color_id=3, image=static("carrier/images/bus04.png"))
        carrier.save()
        carrier = Carrier(name="Alsacia", color_id=4, image=static("carrier/images/bus05.png"))
        carrier.save()
        carrier = Carrier(name="Su Bus", color_id=5, image=static("carrier/images/bus06.png"))
        carrier.save()
        carrier = Carrier(name="Buses Vule", color_id=6, image=static("carrier/images/bus07.png"))
        carrier.save()
        carrier = Carrier(name = "Buses Metropolitana", color_id=7, image=static("carrier/images/bus08.png"))
        carrier.save()