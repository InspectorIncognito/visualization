# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def fill_tables(apps, schema_editor):
    hhperiods = apps.get_model('AndroidRequests', 'HalfHourPeriod')
    hhperiods(name = '00:00 - 00:29', initial_time = '00:00:00', end_time = '00:29:59').save()
    hhperiods(name = '00:30 - 00:59', initial_time = '00:30:00', end_time = '00:59:59').save()
    hhperiods(name = '01:00 - 01:29', initial_time = '01:00:00', end_time = '01:29:59').save()
    hhperiods(name = '01:30 - 01:59', initial_time = '01:30:00', end_time = '01:59:59').save()
    hhperiods(name = '02:00 - 02:29', initial_time = '02:00:00', end_time = '02:29:59').save()
    hhperiods(name = '02:30 - 02:59', initial_time = '02:30:00', end_time = '02:59:59').save()
    hhperiods(name = '03:00 - 03:29', initial_time = '03:00:00', end_time = '03:29:59').save()
    hhperiods(name = '03:30 - 03:59', initial_time = '03:30:00', end_time = '03:59:59').save()
    hhperiods(name = '04:00 - 04:29', initial_time = '04:00:00', end_time = '04:29:59').save()
    hhperiods(name = '04:30 - 04:59', initial_time = '04:30:00', end_time = '04:59:59').save()
    hhperiods(name = '05:00 - 05:29', initial_time = '05:00:00', end_time = '05:29:59').save()
    hhperiods(name = '05:30 - 05:59', initial_time = '05:30:00', end_time = '05:59:59').save()
    hhperiods(name = '06:00 - 06:29', initial_time = '06:00:00', end_time = '06:29:59').save()
    hhperiods(name = '06:30 - 06:59', initial_time = '06:30:00', end_time = '06:59:59').save()
    hhperiods(name = '07:00 - 07:29', initial_time = '07:00:00', end_time = '07:29:59').save()
    hhperiods(name = '07:30 - 07:59', initial_time = '07:30:00', end_time = '07:59:59').save()
    hhperiods(name = '08:00 - 08:29', initial_time = '08:00:00', end_time = '08:29:59').save()
    hhperiods(name = '08:30 - 08:59', initial_time = '08:30:00', end_time = '08:59:59').save()
    hhperiods(name = '09:00 - 09:29', initial_time = '09:00:00', end_time = '09:29:59').save()
    hhperiods(name = '09:30 - 09:59', initial_time = '09:30:00', end_time = '09:59:59').save()
    hhperiods(name = '10:00 - 10:29', initial_time = '10:00:00', end_time = '10:29:59').save()
    hhperiods(name = '10:30 - 10:59', initial_time = '10:30:00', end_time = '10:59:59').save()
    hhperiods(name = '11:00 - 11:29', initial_time = '11:00:00', end_time = '11:29:59').save()
    hhperiods(name = '11:30 - 11:59', initial_time = '11:30:00', end_time = '11:59:59').save()
    hhperiods(name = '12:00 - 12:29', initial_time = '12:00:00', end_time = '12:29:59').save()
    hhperiods(name = '12:30 - 12:59', initial_time = '12:30:00', end_time = '12:59:59').save()
    hhperiods(name = '13:00 - 13:29', initial_time = '13:00:00', end_time = '13:29:59').save()
    hhperiods(name = '13:30 - 13:59', initial_time = '13:30:00', end_time = '13:59:59').save()
    hhperiods(name = '14:00 - 14:29', initial_time = '14:00:00', end_time = '14:29:59').save()
    hhperiods(name = '14:30 - 14:59', initial_time = '14:30:00', end_time = '14:59:59').save()
    hhperiods(name = '15:00 - 15:29', initial_time = '15:00:00', end_time = '15:29:59').save()
    hhperiods(name = '15:30 - 15:59', initial_time = '15:30:00', end_time = '15:59:59').save()
    hhperiods(name = '16:00 - 16:29', initial_time = '16:00:00', end_time = '16:29:59').save()
    hhperiods(name = '16:30 - 16:59', initial_time = '16:30:00', end_time = '16:59:59').save()
    hhperiods(name = '17:00 - 17:29', initial_time = '17:00:00', end_time = '17:29:59').save()
    hhperiods(name = '17:30 - 17:59', initial_time = '17:30:00', end_time = '17:59:59').save()
    hhperiods(name = '18:00 - 18:29', initial_time = '18:00:00', end_time = '18:29:59').save()
    hhperiods(name = '18:30 - 18:59', initial_time = '18:30:00', end_time = '18:59:59').save()
    hhperiods(name = '19:00 - 19:29', initial_time = '19:00:00', end_time = '19:29:59').save()
    hhperiods(name = '19:30 - 19:59', initial_time = '19:30:00', end_time = '19:59:59').save()
    hhperiods(name = '20:00 - 20:29', initial_time = '20:00:00', end_time = '20:29:59').save()
    hhperiods(name = '20:30 - 20:59', initial_time = '20:30:00', end_time = '20:59:59').save()
    hhperiods(name = '21:00 - 21:29', initial_time = '21:00:00', end_time = '21:29:59').save()
    hhperiods(name = '21:30 - 21:59', initial_time = '21:30:00', end_time = '21:59:59').save()
    hhperiods(name = '22:00 - 22:29', initial_time = '22:00:00', end_time = '22:29:59').save()
    hhperiods(name = '22:30 - 22:59', initial_time = '22:30:00', end_time = '22:59:59').save()
    hhperiods(name = '23:00 - 23:29', initial_time = '23:00:00', end_time = '23:29:59').save()
    hhperiods(name = '23:30 - 23:59', initial_time = '23:30:00', end_time = '23:59:59').save()

class Migration(migrations.Migration):

    dependencies = [
        ('AndroidRequests', '0013_auto_20161026_1516'),
    ]

    operations = [
        migrations.CreateModel(
            name='HalfHourPeriod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('initial_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
        ),
        migrations.RunPython(fill_tables, reverse_code=migrations.RunPython.noop),

    ]
