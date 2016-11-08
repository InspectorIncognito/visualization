# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

#Migrates data from StadisticDataFromRegistrationBus

def fill_table(apps, schema_editor):
    stadistics = apps.get_model('AndroidRequests', 'stadisticdatafromregistrationbus')
    eventsForBus = apps.get_model('AndroidRequests', 'EventForBus')
    eventsForBusv2 = apps.get_model('AndroidRequests', 'EventForBusv2')
    buses = apps.get_model('AndroidRequests', 'Bus')
    busesv2 = apps.get_model('AndroidRequests', 'Busv2')
    assignments = apps.get_model('AndroidRequests', 'Busassignment')
    for stadistic in stadistics.objects.all():
        stadistic.reportOfEventv2 = eventsForBusv2.objects.get(ex_id = stadistic.reportOfEvent_id)
        stadistic.save()


class Migration(migrations.Migration):

    dependencies = [
        ('AndroidRequests', '0008_auto_20161011_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='stadisticdatafromregistrationbus',
            name='reportOfEventv2',
            field=models.ForeignKey(verbose_name=b'Bus Event', to='AndroidRequests.EventForBusv2', null=True),
        ),
        migrations.RunPython(fill_table, reverse_code=migrations.RunPython.noop),

        migrations.RemoveField(
            model_name='eventForBusv2',
            name='ex_id',
        ),
    ]
