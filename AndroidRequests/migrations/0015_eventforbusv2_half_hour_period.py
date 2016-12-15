# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc

def fill_tables(apps, schema_editor):
    eventsforbusv2 = apps.get_model('AndroidRequests', 'EventForBusv2')
    eventsforbusstop = apps.get_model('AndroidRequests', 'EventForBusStop')
    hhperiods = apps.get_model('AndroidRequests', 'HalfHourPeriod')
    
    for ev in eventsforbusv2.objects.all():
        time = ev.timeCreation.time().replace(microsecond=0)
        hhperiod = hhperiods.objects.get(initial_time__lte = time , end_time__gte = time)
        ev.half_hour_period = hhperiod
        ev.save()

    for ev in eventsforbusstop.objects.all():
        time = ev.timeCreation.time().replace(microsecond=0)
        hhperiod = hhperiods.objects.get(initial_time__lte = time , end_time__gte = time)
        ev.half_hour_period = hhperiod
        ev.save()

class Migration(migrations.Migration):

    dependencies = [
        ('AndroidRequests', '0014_halfhourperiod'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventforbusv2',
            name='half_hour_period',
            field=models.ForeignKey(verbose_name=b'Half Hour Period', to='AndroidRequests.HalfHourPeriod', null=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventforbusstop',
            name='half_hour_period',
            field=models.ForeignKey(verbose_name=b'Half Hour Period', to='AndroidRequests.HalfHourPeriod', null=True),
            preserve_default=False,
        ),
        migrations.RunPython(fill_tables, reverse_code=migrations.RunPython.noop),

        migrations.AlterField(
            model_name='eventforbusv2',
            name='half_hour_period',
            field=models.ForeignKey(verbose_name=b'Half Hour Period', to='AndroidRequests.HalfHourPeriod', null=False),
        ),
        migrations.AlterField(
            model_name='eventforbusstop',
            name='half_hour_period',
            field=models.ForeignKey(verbose_name=b'Half Hour Period', to='AndroidRequests.HalfHourPeriod', null=False),
        ),
    ]
