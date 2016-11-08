# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('AndroidRequests', '0018_auto_20161107_1448'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zonification',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('area', models.FloatField()),
                ('zona', models.FloatField()),
                ('com', models.CharField(max_length=80)),
                ('comuna', models.CharField(max_length=80)),
                ('cartodb_id', models.IntegerField()),
                ('created_at', models.DateField()),
                ('updated_at', models.DateField()),
                ('comunidad_', models.FloatField(null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=-1)),
            ],
        ),
    ]