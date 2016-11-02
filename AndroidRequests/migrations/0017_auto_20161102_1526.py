# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import json

def fill_table(apps, schema_editor):
	reportsInfo = apps.get_model('AndroidRequests', 'ReportInfo')
	reports = apps.get_model('AndroidRequests', 'Report')
	for report1 in reports.objects.all():
		try:
			reportJson = json.loads(report1.reportInfo)
			if 'bus' in reportJson:
				reportsInfo(
					reportType = 'bus',
					busUUID = reportJson['bus']['machineId'],
					service = reportJson['bus']['service'],
					registrationPlate = reportJson['bus']['licensePlate'],
					latitud = reportJson['bus']['latitude'],
					longitud = reportJson['bus']['longitude'],
					report = report1,
					).save()

			elif 'bus_stop' in reportJson:
				reportsInfo(
					reportType = 'busStop',
					busStopCode = reportJson['bus_stop']['id'],
					latitud = reportJson['bus_stop']['latitude'],
					longitud = reportJson['bus_stop']['longitude'],
					report = report1,
					).save()

			elif 'busStop' in reportJson:
				reportsInfo(
					reportType = 'busStop',
					busStopCode = reportJson['busStop']['id'],
					latitud = reportJson['busStop']['latitude'],
					longitud = reportJson['busStop']['longitude'],
					report = report1,
					).save()

		except ValueError:
			pass
    

class Migration(migrations.Migration):

    dependencies = [
        ('AndroidRequests', '0016_reportinfo'),
    ]

    operations = [
    	migrations.RunPython(fill_table, reverse_code=migrations.RunPython.noop),
    ]
