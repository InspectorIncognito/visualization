# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import re

#Add validation for the license plates.

def fill_tables(apps, schema_editor):
	buses = apps.get_model('AndroidRequests', 'Busv2')
	ex = r"\A[a-zA-Z]{4}[0-9]{2}\Z|\A[a-zA-Z]{2}[0-9]{4}\Z"
	regex = re.compile(ex)
	for bus in buses.objects.all():
		if bus.registrationPlate.upper() == 'DUMMYLPT':
			bus.registrationPlate = "No Info."
		elif regex.match(bus.registrationPlate.upper()) != None :
			aa = bus.registrationPlate[:2].upper()
			bb = bus.registrationPlate[2:4].upper()
			num = bus.registrationPlate[4:]
			bus.registrationPlate = aa+" "+bb+" "+num
		else:
			pass

		bus.save()
    

class Migration(migrations.Migration):

    dependencies = [
        ('AndroidRequests', '0012_auto_20161025_1619'),
    ]

    operations = [
    	migrations.RunPython(fill_tables, reverse_code=migrations.RunPython.noop),
    ]
