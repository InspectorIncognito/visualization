# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

#Add the link between TimePeriod and the Events tables.

def fill_tables(apps, schema_editor):
    eventsforbusv2 = apps.get_model('AndroidRequests', 'EventForBusv2')
    eventsforbusstop = apps.get_model('AndroidRequests', 'EventForBusStop')
    timeperiods = apps.get_model('AndroidRequests', 'TimePeriod')
    
    for ev in eventsforbusv2.objects.all():
        time = ev.timeCreation.time().replace(microsecond=0)
        timeperiod = None
        if ev.timeCreation.strftime("%A") == 'Saturday':
            timeperiod = timeperiods.objects.get(
                day_type = 'Sábado',
                initial_time__lte = time ,
                end_time__gte = time
            )
        elif ev.timeCreation.strftime("%A") == 'Sunday':
            timeperiod = timeperiods.objects.get(
                day_type = 'Domingo',
                initial_time__lte = time,
                end_time__gte = time
            )
        else:
            #Working day
            timeperiod = timeperiods.objects.get(
                day_type = 'Laboral',
                initial_time__lte = time ,
                end_time__gte = time
            )

        ev.timePeriod = timeperiod
        ev.save()

    for ev in eventsforbusstop.objects.all():
        time = ev.timeCreation.time().replace(microsecond=0)
        timeperiod = None
        if ev.timeCreation.strftime("%A") == 'Saturday':
            timeperiod = timeperiods.objects.get(
                day_type = 'Sábado',
                initial_time__lte = time ,
                end_time__gte = time
            )
        elif ev.timeCreation.strftime("%A") == 'Sunday':
            timeperiod = timeperiods.objects.get(
                day_type = 'Domingo',
                initial_time__lte = time ,
                end_time__gte = time
            )
        else:
            #Working day
            timeperiod = timeperiods.objects.get(
                day_type = 'Laboral',
                initial_time__lte = time ,
                end_time__gte = time
            )

        ev.timePeriod = timeperiod
        ev.save()

class Migration(migrations.Migration):

    dependencies = [
        ('AndroidRequests', '0900_transformation_20161025_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventforbusv2',
            name='timePeriod',
            field=models.ForeignKey(verbose_name=b'Time Period',
                                    to='AndroidRequests.TimePeriod',
                                    null = True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventforbusstop',
            name='timePeriod',
            field=models.ForeignKey(verbose_name=b'Time Period',
                                    to='AndroidRequests.TimePeriod',
                                    null = True),
            preserve_default=False,
        ),
        migrations.RunPython(fill_tables, reverse_code=migrations.RunPython.noop),

        migrations.AlterField(
            model_name='eventforbusv2',
            name='timePeriod',
            field=models.ForeignKey(verbose_name=b'Time Period',
                                    to='AndroidRequests.TimePeriod',
                                    null = False),
        ),
        migrations.AlterField(
            model_name='eventforbusstop',
            name='timePeriod',
            field=models.ForeignKey(verbose_name=b'Time Period',
                                    to='AndroidRequests.TimePeriod',
                                    null = False),
        ),
        migrations.AddField(
            model_name='eventforbusstop',
            name='fixed',
            field=models.BooleanField(default=False, verbose_name=b'Fixed'),
        ),
        migrations.AddField(
            model_name='eventforbusv2',
            name='fixed',
            field=models.BooleanField(default=False, verbose_name=b'Fixed'),
        ),
    ]
