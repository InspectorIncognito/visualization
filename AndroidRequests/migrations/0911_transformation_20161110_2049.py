# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('AndroidRequests', '0910_transformation_nearest_busstops'),
    ]

    operations = [
        migrations.AlterField(
            model_name='busstop',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(srid=32140, verbose_name=b'The point'),
        ),
        migrations.AlterField(
            model_name='eventforbusv2',
            name='busStop1',
            field=models.ForeignKey(related_name='busStop1', verbose_name=b'Bus Stop1', to='AndroidRequests.BusStop'),
        ),
        migrations.AlterField(
            model_name='eventforbusv2',
            name='busStop2',
            field=models.ForeignKey(related_name='busStop2', verbose_name=b'Bus Stop2', to='AndroidRequests.BusStop'),
        ),
    ]
