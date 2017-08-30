# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from transform import WITHOUT_LICENSE_PLATE

import json

#Loads the JSON info in the reports into the ReportInfo table

def fill_table(apps, schema_editor):
    reportsInfo = apps.get_model('AndroidRequests', 'ReportInfo')
    reports = apps.get_model('AndroidRequests', 'Report')
    buses = apps.get_model('AndroidRequests', 'Busv2')
    for report1 in reports.objects.all():
        if report1.reportInfo is None or report1.reportInfo == "":
            continue

        reportJson = json.loads(report1.reportInfo)
        if 'bus' in reportJson:
            licensePlate = reportJson['bus']['licensePlate']
            if reportJson['bus']['licensePlate'].upper() == "DUMMYLPT":
                plate = WITHOUT_LICENSE_PLATE
            elif licensePlate[2] == " " and licensePlate[5] == " ":
                plate = licensePlate.upper()
            else:
                aa = licensePlate[:2].upper()
                bb = licensePlate[2:4].upper()
                num = licensePlate[4:]
                plate = aa + " " + bb + " " + num

            if "machineId" in reportJson["bus"] and reportJson['bus']['machineId'] != "":
                busUUIDn = reportJson['bus']['machineId']
            elif buses.objects.filter(registrationPlate = plate).count() == 1:
                busUUIDn = buses.objects.filter(registrationPlate=plate).values_list("uuid", flat=True)[0]
            else:
                busUUIDn = None

            if busUUIDn is not None:
                plate = buses.objects.filter(uuid=busUUIDn).values_list("registrationPlate", flat=True)[0]

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


class Migration(migrations.Migration):

    dependencies = [
        ('AndroidRequests', '0905_transformation_reportinfo'),
    ]

    operations = [
        migrations.RunPython(fill_table, reverse_code=migrations.RunPython.noop),
    ]
