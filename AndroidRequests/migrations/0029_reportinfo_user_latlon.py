# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import json


def fill_tables(apps, schema_editor):

    report_info_array = apps.get_model('AndroidRequests', 'ReportInfo')
    for report_info in report_info_array.objects.all():

        try:
            # user location from json field
            report_json = json.loads(report_info.report.reportInfo)
            user_location = report_json['locationUser']
            lat_str = user_location['latitude']
            lon_str = user_location['longitude']

            # parsing
            # data is kept as follows: "\/-33.75654"
            user_latitude = float(lat_str[1:])
            user_longitude = float(lon_str[1:])

            # save
            report_info.userLatitude = user_latitude
            report_info.userLongitude = user_longitude
            report_info.save()
        except:
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('AndroidRequests', '0028_reportinfo_foreign_busstop'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportinfo',
            name='userLatitude',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='reportinfo',
            name='userLongitude',
            field=models.FloatField(null=True),
        ),
        migrations.RunPython(fill_tables, reverse_code=migrations.RunPython.noop)
    ]
