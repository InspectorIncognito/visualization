# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.gis.geos import Point

#Add the county to the Events and ReportInfo tables.

def fill_tables(apps, schema_editor):
    eventsforbusv2 = apps.get_model('AndroidRequests', 'EventForBusv2')
    eventsforbusstop = apps.get_model('AndroidRequests', 'EventForBusStop')
    reportsinfo = apps.get_model('AndroidRequests', 'ReportInfo')
    statisticsfrombus = apps.get_model('AndroidRequests', 'StadisticDataFromRegistrationBus')
    statisticsfrombusstop = apps.get_model('AndroidRequests', 'StadisticDataFromRegistrationBusStop')
    zonification = apps.get_model('AndroidRequests', 'zonificationTransantiago')

    for st in statisticsfrombus.objects.all():
        aux = st.latitud
        st.latitud = st.longitud
        st.longitud = aux
        st.save()

    print("ZONIFICACION DE EVENTS FOR BUS")
    for ev in eventsforbusv2.objects.all():
        statistic_data = statisticsfrombus.objects.filter(reportOfEvent = ev).order_by('-timeStamp')[0]
        ev_lat = statistic_data.latitud
        ev_long = statistic_data.longitud
        pnt = Point(ev_long, ev_lat)
        zon = None
        try:
            zon = zonification.objects.filter(geom__intersects = pnt)[0]
        except:
            pass
        ev.zonification = zon
        ev.save()
    
    print("ZONIFICACION DE EVENTS FOR BUS STOP")
    for ev in eventsforbusstop.objects.all():
        statistic_data = statisticsfrombusstop.objects.filter(reportOfEvent = ev).order_by('-timeStamp')[0]
        ev_lat = statistic_data.latitud
        ev_long = statistic_data.longitud
        pnt = Point(ev_long, ev_lat)
        zon = None
        try:
            zon = zonification.objects.filter(geom__intersects = pnt)[0]
        except:
            pass
        ev.zonification = zon
        ev.save()

    print("ZONIFICACION DE REPORT INFO")
    for ev in reportsinfo.objects.all():

        pnt = Point(ev.longitud, ev.latitud)
        zon = None
        try:
            zon = zonification.objects.filter(geom__intersects = pnt)[0]
        except:
            pass
        ev.zonification = zon
        ev.save()

class Migration(migrations.Migration):

    dependencies = [
        ('AndroidRequests', '0019_zonification'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventforbusv2',
            name='zonification',
            field=models.ForeignKey('zonificationTransantiago', verbose_name='zonification', null = True),
    
        ),
        migrations.AddField(
            model_name='eventforbusstop',
            name='zonification',
            field=models.ForeignKey('zonificationTransantiago', verbose_name='zonification', null = True),
        ),
        migrations.AddField(
            model_name='reportinfo',
            name='zonification',
            field=models.ForeignKey('zonificationTransantiago', verbose_name='zonification', null = True),
        ),
        migrations.RunPython(fill_tables, reverse_code=migrations.RunPython.noop),
    ]

