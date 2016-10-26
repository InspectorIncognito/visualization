# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import re

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
    # eventsforbusv2 = apps.get_model('AndroidRequests', 'EventForBusv2')
    # timeperiods = apps.get_model('AndroidRequests', 'TimePeriod')
    
    # for ev in eventsforbusv2.objects.all():
    #     # time_to_match = ev.timeCreation
    #     # print(time_to_match)
    #     time = ev.timeCreation.time()
    #     timeperiod = None
    #     if ev.timeCreation.strftime("%A") == 'Saturday':
    #         timeperiod = timeperiods.objects.get(day_type = 'Sabado',\
    #             initial_time__lte = time , end_time__gt = time)
    #     elif ev.timeCreation.strftime("%A") == 'Sunday':
    #         timeperiod = timeperiods.objects.get(day_type = 'Domingo',\
    #             initial_time__lte = time , end_time__gt = time)
    #     else:
    #         #Working day
    #         timeperiod = timeperiods.objects.get(day_type = 'Laboral',\
    #             initial_time__lte = time , end_time__gt = time)

    #     ev.time_period = timeperiod
    #     ev.save()

class Migration(migrations.Migration):

    dependencies = [
        ('AndroidRequests', '0012_auto_20161025_1619'),
    ]

    operations = [
    	migrations.RunPython(fill_tables, reverse_code=migrations.RunPython.noop),
    ]
