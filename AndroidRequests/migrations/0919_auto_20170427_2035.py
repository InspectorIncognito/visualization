# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-27 20:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AndroidRequests', '0918_transformation_reportinfo_user_latlon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventforbusstop',
            name='zonification',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AndroidRequests.ZonificationTransantiago', verbose_name=b'zonification'),
        ),
        migrations.AlterField(
            model_name='eventforbusv2',
            name='zonification',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AndroidRequests.ZonificationTransantiago', verbose_name=b'zonification'),
        ),
        migrations.AlterField(
            model_name='reportinfo',
            name='zonification',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='AndroidRequests.ZonificationTransantiago', verbose_name=b'zonification'),
        ),
        migrations.AlterField(
            model_name='reportinfo',
            name='stopCode',
            field=models.CharField(max_length=6, null=True, verbose_name=b'StopCode'),
        ),
        #migrations.AlterUniqueTogether(
        #    name='busassignment',
        #    unique_together=set(['uuid', 'service']),
        #),
    ]
