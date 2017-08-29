# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from datetime import timedelta
from django.utils import timezone
from pytz import timezone as tz

def set_expire_time_and_add_timezone(apps, schema_editor):

    local = tz("America/Santiago")

    bus_events = apps.get_model('AndroidRequests', 'EventForBusv2')
    stop_events = apps.get_model('AndroidRequests', 'EventForBusStop')
    events = apps.get_model('AndroidRequests', 'Event')

    event_dict = {e.id: e.lifespam for e in events.objects.all()}

    for bus_event in bus_events.objects.all():
        if timezone.is_naive(bus_event.timeCreation):
            bus_event.timeCreation = local.localize(bus_event.timeCreation)
        if timezone.is_naive(bus_event.timeStamp):
            bus_event.timeStamp = local.localize(bus_event.timeStamp)

        if bus_event.expireTime is None:
            bus_event.expireTime = bus_event.timeStamp + timedelta(minutes=event_dict[bus_event.event_id])
        elif timezone.is_naive(bus_event.expireTime):
            bus_event.expireTime = local.localize(bus_event.expireTime)

        bus_event.save()

    for stop_event in stop_events.objects.all():
        if timezone.is_naive(stop_event.timeCreation):
            stop_event.timeCreation = local.localize(stop_event.timeCreation)
        if timezone.is_naive(stop_event.timeStamp):
            stop_event.timeStamp = local.localize(stop_event.timeStamp)

        if stop_event.expireTime is None:
            stop_event.expireTime = stop_event.timeStamp + timedelta(minutes=event_dict[stop_event.event_id])
        elif timezone.is_naive(stop_event.expireTime):
            stop_event.expireTime = local.localize(stop_event.expireTime)

        stop_event.save()


class Migration(migrations.Migration):

    dependencies = [
        ('AndroidRequests', '0919_auto_20170427_2035'),
    ]

    operations = [
        migrations.RunPython(set_expire_time_and_add_timezone, reverse_code=migrations.RunPython.noop)
    ]
