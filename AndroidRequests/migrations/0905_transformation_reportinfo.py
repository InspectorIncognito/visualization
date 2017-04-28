# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AndroidRequests', '0904_transformation_eventforbusv2_half_hour_period'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reportType', models.CharField(max_length=7, verbose_name=b'Event Type', 
                    choices=[(b'bus', b'An event for the bus.'), (b'busStop', b'An event for the busStop.')])),
                ('busUUID', models.UUIDField(null=True)),
                ('service', models.CharField(max_length=11, null=True, verbose_name=b'Service')),
                ('registrationPlate', models.CharField(max_length=8)),
                ('stopCode', models.CharField(max_length=6, null=True, verbose_name=b'Code')),
                ('longitude', models.FloatField(verbose_name=b'Longitude')),
                ('latitude', models.FloatField(verbose_name=b'Latitude')),
                ('report', models.ForeignKey(verbose_name=b'The Report', to='AndroidRequests.Report')),
            ],
        ),
    ]
