# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from math import cos, asin, sqrt
from django.contrib.gis.geos import Point
from django.contrib.gis.db import models
import sys

#def distance(lat1, lon1, lat2, lon2):
#    p = 0.017453292519943295
#    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
#    return 12742 * asin(sqrt(a))

def fill_tables(apps, schema_editor):
    eventsforbusv2 = apps.get_model('AndroidRequests', 'EventForBusv2')
    busstops = apps.get_model('AndroidRequests', 'BusStop')
    statisticsfrombus = apps.get_model('AndroidRequests', 'StadisticDataFromRegistrationBus')
    zonification = apps.get_model('AndroidRequests', 'zonificationTransantiago')
    sys.stdout.write("\nBusStop iteration\nTotal rows: "+str(busstops.objects.all().count())+"\n")
    sys.stdout.write("\r Rows modified: 0")
    sys.stdout.flush()
    counter = 0
    for busstop in busstops.objects.all():
        busstop.point = Point(busstop.longitud, busstop.latitud)
        #print("creando point")
        busstop.save()
        counter = counter + 1
        if counter%100==0:
            sys.stdout.write("\r Rows modified: "+str(counter))
            sys.stdout.flush()
    sys.stdout.write("\n Total rows modified: "+str(counter) + "\n")
    #print("points creados")
    busstopsdict = busstops.objects.values()
    sys.stdout.write("\nEvents for Bus iteration\nTotal rows: "+str(eventsforbusv2.objects.all().count())+"\n")
    sys.stdout.write("\r Rows modified: 0")
    sys.stdout.flush()
    counter = 0
    for ev in eventsforbusv2.objects.all():
        nearest = []
        statistic_data = statisticsfrombus.objects.filter(reportOfEvent = ev).order_by('-timeStamp')[0]
        ev_lat = statistic_data.latitud
        ev_long = statistic_data.longitud
        evpoint = Point(ev_long, ev_lat)
        for busstop in busstopsdict:
            busstop["distance"] = busstop['point'].distance(evpoint)
        nearest = sorted(busstopsdict, key = lambda busstop: busstop['distance'])
        ev.busStop1 = busstops.objects.get(code = nearest[0]['code'])
        ev.busStop2 = busstops.objects.get(code = nearest[1]['code'])
        ev.save()
        counter = counter +1
        if counter%100==0:
            sys.stdout.write("\r Rows modified: "+str(counter))
            sys.stdout.flush()
        # aux = 0
        # for near in nearest:
        #     if near['distance'] > aux:
        #         aux = near['distance']
        #     else:
        #         raise ValueError("ERROR: El anterior era mayor o igual que el actual")
        # nearest = busstops.objects.distance(evpoint)
        # print("event    -    lat: " + ev_lat +" long: " + ev_long)
        # print("nearest0  -    lat: " + nearest[0].latitud + " long: " + nearest[0].longitud)
        # print("nearest1  -    lat: " + nearest[1].latitud + " long: " + nearest[1].longitud)
        #raise ValueError('Hola, soy una exception')
        #TODO: Calculate the distance between the points of latitude and longitude
        #https://en.wikipedia.org/wiki/Haversine_formula
        #ev.save()
    #raise ValueError('Hola, soy una exception')
    sys.stdout.write("\n Total rows modified: "+str(counter) + "\n")

class Migration(migrations.Migration):

    dependencies = [
        ('AndroidRequests', '0020_auto_20161107_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventforbusv2',
            name='busStop1',
            field=models.ForeignKey(related_name='busStop1', verbose_name=b'Bus Stop1', to='AndroidRequests.BusStop', null=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventforbusv2',
            name='busStop2',
            field=models.ForeignKey(related_name='busStop2', verbose_name=b'Bus Stop2', to='AndroidRequests.BusStop', null=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='busstop',
            name='point',
            field = models.PointField(srid=32140, verbose_name='The point', null = True),
            preserve_default=False,
        ),
        migrations.RunPython(fill_tables, reverse_code=migrations.RunPython.noop),
        
    ]
