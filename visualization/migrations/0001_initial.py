# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def fill_tables(apps, schema_editor):
	timeperiods = apps.get_model('visualization', 'timeperiod')
	timeperiods(day_type = 'Laboral', name = 'Pre nocturno', initial_time = '00:00:00', end_time = '00:59:59').save()
	timeperiods(day_type = 'Laboral', name = 'Nocturno', initial_time = '01:00:00', end_time = '05:29:59').save()
	timeperiods(day_type = 'Laboral', name = 'Transicion nocturno', initial_time = '05:30:00', end_time = '06:29:59').save()
	timeperiods(day_type = 'Laboral', name = 'Punta mañana', initial_time = '06:30:00', end_time = '08:29:59').save()
	timeperiods(day_type = 'Laboral', name = 'Transicion punta mañana', initial_time = '08:30:00', end_time = '09:29:59').save()
	timeperiods(day_type = 'Laboral', name = 'Fuera de punta mañana', initial_time = '09:30:00', end_time = '12:29:59').save()
	timeperiods(day_type = 'Laboral', name = 'Punta mediodia', initial_time = '12:30:00', end_time = '13:59:59').save()
	timeperiods(day_type = 'Laboral', name = 'Fuera de punta tarde', initial_time = '14:00:00', end_time = '17:29:59').save()
	timeperiods(day_type = 'Laboral', name = 'Punta tarde', initial_time = '17:30:00', end_time = '20:29:59').save()
	timeperiods(day_type = 'Laboral', name = 'Transicion punta tarde', initial_time = '20:30:00', end_time = '21:29:59').save()
	timeperiods(day_type = 'Laboral', name = 'Fuera de punta nocturno', initial_time = '21:30:00', end_time = '22:59:59').save()
	timeperiods(day_type = 'Laboral', name = 'Pre nocturno', initial_time = '23:00:00', end_time = '23:59:59').save()
	timeperiods(day_type = 'Sabado', name = 'Pre nocturno sabado', initial_time = '00:00:00', end_time = '00:59:59').save()
	timeperiods(day_type = 'Sabado', name = 'Nocturno sabado', initial_time = '01:00:00', end_time = '05:29:59').save()
	timeperiods(day_type = 'Sabado', name = 'Transicion sabado mañana', initial_time = '05:30:00', end_time = '06:29:59').save()
	timeperiods(day_type = 'Sabado', name = 'Punta mañana sabado', initial_time = '06:30:00', end_time = '10:59:59').save()
	timeperiods(day_type = 'Sabado', name = 'Mañana sabado', initial_time = '11:00:00', end_time = '13:29:59').save()
	timeperiods(day_type = 'Sabado', name = 'Punta mediodia sabado', initial_time = '13:30:00', end_time = '17:29:59').save()
	timeperiods(day_type = 'Sabado', name = 'Tarde sabado', initial_time = '17:30:00', end_time = '20:29:59').save()
	timeperiods(day_type = 'Sabado', name = 'Transicion sabado nocturno', initial_time = '20:30:00', end_time = '22:59:59').save()
	timeperiods(day_type = 'Sabado', name = 'Pre nocturno sabado', initial_time = '23:00:00', end_time = '22:59:59').save()
	timeperiods(day_type = 'Domingo', name = 'Pre nocturno domingo', initial_time = '00:00:00', end_time = '00:59:59').save()
	timeperiods(day_type = 'Domingo', name = 'Nocturno domingo', initial_time = '01:00:00', end_time = '05:29:5905:30:00').save()
	timeperiods(day_type = 'Domingo', name = 'Transicion domingo mañana', initial_time = '05:30:00', end_time = '09:29:59').save()
	timeperiods(day_type = 'Domingo', name = 'Mañana domingo', initial_time = '09:30:00', end_time = '13:29:59').save()
	timeperiods(day_type = 'Domingo', name = 'Mediodia domingo', initial_time = '13:30:00', end_time = '17:29:59').save()
	timeperiods(day_type = 'Domingo', name = 'Tarde domingo', initial_time = '17:30:00', end_time = '20:59:59').save()
	timeperiods(day_type = 'Domingo', name = 'Transicion domingo', initial_time = '21:00:00', end_time = '22:59:59').save()
	timeperiods(day_type = 'Domingo', name = 'Pre nocturno domingo', initial_time = '23:00:00', end_time = '23:59:59').save()


class Migration(migrations.Migration):

    dependencies = [
    ]

    # Posibles operaciones que querriamos realizar:
    # 1. Borrar tablas innecesarias para visualizacion
    # 2. Dejar solo los modelos V2
    # 3. Cambiar nombres de tablas
    operations = [
        migrations.CreateModel(
            name='TimePeriod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day_type', models.CharField(max_length=8)),
                ('name', models.CharField(max_length=30)),
                ('initial_time', models.TimeField(auto_now=False, auto_now_add=False)),
                ('end_time', models.TimeField(auto_now=False, auto_now_add=False)),
            ],
        ),
        migrations.RunPython(fill_tables, reverse_code=migrations.RunPython.noop),
    ]
