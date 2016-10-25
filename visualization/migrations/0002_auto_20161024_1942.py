# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def fill_tables(apps, schema_editor):
	eventsforbusv2 = apps.get_model('visualization', 'eventsforbusv2')
	for ev in eventsforbusv2.objects.all():
		time_to_match = ev.timeCreation
		print(time_to_match)

class Migration(migrations.Migration):

    dependencies = [
        ('visualization', '0001_initial'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='eventforbusv2',
        #     name='time_period',
        #     field=models.ForeignKey(verbose_name=b'Time Period', to='visualization.EventForBusv2', null = True),
        #     preserve_default=False,
        # ),
        migrations.RunPython(fill_tables, reverse_code=migrations.RunPython.noop),
    ]
