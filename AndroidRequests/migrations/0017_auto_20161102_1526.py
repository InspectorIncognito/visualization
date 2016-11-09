# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import json

#Loads the JSON info in the reports into the ReportInfo table

def fill_table(apps, schema_editor):
	reportsInfo = apps.get_model('AndroidRequests', 'ReportInfo')
	reports = apps.get_model('AndroidRequests', 'Report')
	buses = apps.get_model('AndroidRequests', 'Busv2')
	for report1 in reports.objects.all():
		print(report1.pk)
		try:
			reportJson = json.loads(report1.reportInfo)
			if 'bus' in reportJson:
				aa = reportJson['bus']['licensePlate'][:2].upper()
				bb = reportJson['bus']['licensePlate'][2:4].upper()
				num = reportJson['bus']['licensePlate'][4:]
				plate = aa + " " + bb + " " + num
				busUUIDn = None
				try:
					busUUIDn = reportJson['bus']['machineId']
				except:
					if reportJson['bus']['licensePlate'].upper() != "DUMMYLPT":
						busUUIDn = buses.objects.get(registrationPlate = plate).uuid
				if reportJson['bus']['licensePlate'].upper() == "DUMMYLPT":
					plate = reportJson['bus']['licensePlate'].upper()
				reportinfo = reportsInfo(
					reportType = 'bus',
					busUUID = busUUIDn,
					service = reportJson['bus']['service'],
					registrationPlate = plate,
					latitud = reportJson['bus']['latitude'],
					longitud = reportJson['bus']['longitude'],
					report = report1,
					)
				reportinfo.save()

			elif 'bus_stop' in reportJson:
				reportinfo = reportsInfo(
					reportType = 'busStop',
					busStopCode = reportJson['bus_stop']['id'],
					latitud = reportJson['bus_stop']['latitude'],
					longitud = reportJson['bus_stop']['longitude'],
					report = report1,
					)
				reportinfo.save()

			elif 'busStop' in reportJson:
				reportinfo = reportsInfo(
					reportType = 'busStop',
					busStopCode = reportJson['busStop']['id'],
					latitud = reportJson['busStop']['latitude'],
					longitud = reportJson['busStop']['longitude'],
					report = report1,
					)
				reportinfo.save()

		except ValueError:
			pass
    

class Migration(migrations.Migration):

    dependencies = [
        ('AndroidRequests', '0016_reportinfo'),
    ]

    operations = [
    	migrations.RunPython(fill_table, reverse_code=migrations.RunPython.noop),
    ]
