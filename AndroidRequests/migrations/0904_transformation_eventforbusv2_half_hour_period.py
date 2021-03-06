# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone

from django.db import models, migrations

def fill_tables(apps, schema_editor):
    eventsforbusv2 = apps.get_model('AndroidRequests', 'EventForBusv2')
    eventsforbusstop = apps.get_model('AndroidRequests', 'EventForBusStop')
    hhperiods = apps.get_model('AndroidRequests', 'HalfHourPeriod')
    
    for ev in eventsforbusv2.objects.all():
        creationTime = timezone.localtime(ev.timeCreation).time().replace(microsecond=0)
        hhperiod = hhperiods.objects.get(initial_time__lte = creationTime , end_time__gte = creationTime)
        ev.halfHourPeriod = hhperiod
        ev.save()

    for ev in eventsforbusstop.objects.all():
        creationTime = timezone.localtime(ev.timeCreation).time().replace(microsecond=0)
        hhperiod = hhperiods.objects.get(initial_time__lte = creationTime , end_time__gte = creationTime)
        ev.halfHourPeriod = hhperiod
        ev.save()

class Migration(migrations.Migration):

    dependencies = [
        ('AndroidRequests', '0903_transformation_halfhourperiod'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventforbusv2',
            name='halfHourPeriod',
            field=models.ForeignKey(verbose_name=b'Half Hour Period', to='AndroidRequests.HalfHourPeriod', null=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventforbusstop',
            name='halfHourPeriod',
            field=models.ForeignKey(verbose_name=b'Half Hour Period', to='AndroidRequests.HalfHourPeriod', null=True),
            preserve_default=False,
        ),
        migrations.RunPython(fill_tables, reverse_code=migrations.RunPython.noop),

        migrations.AlterField(
            model_name='eventforbusv2',
            name='halfHourPeriod',
            field=models.ForeignKey(verbose_name=b'Half Hour Period', to='AndroidRequests.HalfHourPeriod', null=False),
        ),
        migrations.AlterField(
            model_name='eventforbusstop',
            name='halfHourPeriod',
            field=models.ForeignKey(verbose_name=b'Half Hour Period', to='AndroidRequests.HalfHourPeriod', null=False),
        ),
    ]
