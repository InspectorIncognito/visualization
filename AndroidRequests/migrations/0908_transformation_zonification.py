# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
import AndroidRequests.load777zonification

def fill_tables(apps, schema_editor):
    AndroidRequests.load777zonification.run()

class Migration(migrations.Migration):

    dependencies = [
        ('AndroidRequests', '0907_transformation_20161107_1448'),
    ]

    operations = [
        migrations.CreateModel(
            name='zonificationTransantiago',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('area', models.FloatField()),
                ('zona', models.FloatField()),
                ('com', models.CharField(max_length=80)),
                ('comuna', models.CharField(max_length=80)),
                ('cartodb_id', models.IntegerField()),
                ('created_at', models.DateField()),
                ('updated_at', models.DateField()),
                ('comunidad_field', models.FloatField(null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
        ),
        migrations.RunPython(fill_tables, reverse_code=migrations.RunPython.noop),
    ]
