# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AndroidRequests', '0916_transformation_20161219_1848'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reportinfo',
            old_name='busStopCode',
            new_name='busStop',
        ),
        migrations.AlterField(
            model_name='reportinfo',
            name='busStop',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='AndroidRequests.BusStop'
            ),
        ),
    ]
