# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from math import cos, asin, sqrt

def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))

def fill_tables(apps, schema_editor):
    eventsforbusv2 = apps.get_model('AndroidRequests', 'EventForBusv2')
    busstops = apps.get_model('AndroidRequests', 'BusStop')
    statisticsfrombus = apps.get_model('AndroidRequests', 'StadisticDataFromRegistrationBus')
    zonification = apps.get_model('AndroidRequests', 'zonificationTransantiago')

    for ev in eventsforbusv2.objects.all():
        statistic_data = statisticsfrombus.objects.filter(reportOfEvent = ev).order_by('-timeStamp')[0]
        ev_lat = statistic_data.latitud
        ev_long = statistic_data.longitud
        #TODO: Calculate the distance between the points of latitude and longitude
        #https://en.wikipedia.org/wiki/Haversine_formula
        #ev.save()

class Migration(migrations.Migration):

    dependencies = [
        ('AndroidRequests', '0020_auto_20161107_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventforbusv2',
            name='busStop1',
            field=models.ForeignKey(related_name='busStop1', default=1, verbose_name=b'Bus Stop1', to='AndroidRequests.BusStop'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventforbusv2',
            name='busStop2',
            field=models.ForeignKey(related_name='busStop2', default=1, verbose_name=b'Bus Stop2', to='AndroidRequests.BusStop'),
            preserve_default=False,
        ),
        migrations.RunPython(fill_tables, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name='eventforbusv2',
            name='busStop1',
            field=models.ForeignKey(related_name='busStop1', verbose_name=b'Bus Stop1', to='AndroidRequests.BusStop'),
        ),
        migrations.AlterField(
            model_name='eventforbusv2',
            name='busStop2',
            field=models.ForeignKey(related_name='busStop2', verbose_name=b'Bus Stop2', to='AndroidRequests.BusStop'),
        ),
    ]
