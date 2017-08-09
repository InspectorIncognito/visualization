# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models, migrations
import json


#Loads the JSON info in the reports into the ReportInfo table

def fill_table(apps, schema_editor):
    reportsInfo = apps.get_model('AndroidRequests', 'ReportInfo')
    reports = apps.get_model('AndroidRequests', 'Report')
    buses = apps.get_model('AndroidRequests', 'Busv2')
    for report1 in reports.objects.all():

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
                    if busUUIDn == "" and buses.objects.filter(registrationPlate = plate).count() == 1:
                        busUUIDn = buses.objects.filter(registrationPlate = plate).values_list("uuid", flat=True)[0]
                    else:
                        continue
                except:
                    if reportJson['bus']['licensePlate'].upper() != "DUMMYLPT":
                        busUUIDn = buses.objects.filter(registrationPlate = plate).values_list("uuid", flat=True)[0]
                if reportJson['bus']['licensePlate'].upper() == "DUMMYLPT":
                    plate = reportJson['bus']['licensePlate'] = 'No Info.'
                if len(reportJson['bus']['service']) > 5:
                    reportJson['bus']['service'] = '-'
                reportsInfo.objects.create(
                    reportType = 'bus',
                    busUUID = busUUIDn,
                    service = reportJson['bus']['service'],
                    registrationPlate = plate,
                    latitude = reportJson['bus']['latitude'],
                    longitude = reportJson['bus']['longitude'],
                    report = report1)

            elif 'bus_stop' in reportJson:
                reportsInfo.objects.create(
                    reportType = 'busStop',
                    stopCode = reportJson['bus_stop']['id'],
                    latitude = reportJson['bus_stop']['latitude'],
                    longitude = reportJson['bus_stop']['longitude'],
                    report = report1)

            elif 'busStop' in reportJson:
                reportsInfo.objects.create(
                    reportType = 'busStop',
                    stopCode = reportJson['busStop']['id'],
                    latitude = reportJson['busStop']['latitude'],
                    longitude = reportJson['busStop']['longitude'],
                    report = report1)

        except (ValueError, ValidationError) as e:
            print("Error: {}".format(str(e)))
    

class Migration(migrations.Migration):

    dependencies = [
        ('AndroidRequests', '0905_transformation_reportinfo'),
    ]

    operations = [
        migrations.RunPython(fill_table, reverse_code=migrations.RunPython.noop),
    ]
