# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.gis.geos import Point

def fill_tables(apps, schema_editor):
    eventsforbusv2 = apps.get_model('AndroidRequests', 'EventForBusv2')
    eventsforbusstop = apps.get_model('AndroidRequests', 'EventForBusStop')
    statisticsfrombus = apps.get_model('AndroidRequests', 'StadisticDataFromRegistrationBus')
    statisticsfrombusstop = apps.get_model('AndroidRequests', 'StadisticDataFromRegistrationBusStop')
    zonification = apps.get_model('AndroidRequests', 'zonificationTransantiago')

    for ev in eventsforbusv2.objects.all():
        statistic_data = statisticsfrombus.objects.filter(reportOfEvent = ev).order_by('-timeStamp')[0]
        ev_lat = statistic_data.latitud
        ev_long = statistic_data.longitud
        # pnt = 'POINT('+str(ev_long)+' '+str(ev_lat)+')'
        pnt = Point(ev_lat, ev_long)
        county = "Fuera de la zona"
        try:
            county = zonification.objects.filter(geom__intersects = pnt)[0].comuna
        except:
            pass
        ev.county = county
        ev.save()
    
    for ev in eventsforbusstop.objects.all():
        statistic_data = statisticsfrombusstop.objects.filter(reportOfEvent = ev).order_by('-timeStamp')[0]
        ev_lat = statistic_data.latitud
        ev_long = statistic_data.longitud
        pnt = Point(ev_lat, ev_long)
        county = "Fuera de la zona"
        try:
            county = zonification.objects.filter(geom__intersects = pnt)[0].comuna
        except:
            pass
        ev.county = county
        ev.save()

class Migration(migrations.Migration):

    dependencies = [
        ('AndroidRequests', '0019_zonification'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventforbusv2',
            name='county',
            field=models.CharField(max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='eventforbusstop',
            name='county',
            field=models.CharField(max_length=80, null=True),
        ),
        migrations.RunPython(fill_tables, reverse_code=migrations.RunPython.noop),
    ]

