# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-16 19:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AndroidRequests', '0913_transformation_20161215_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='busstop',
            name='transformed',
            field=models.NullBooleanField(default=False, verbose_name=b'Transformed'),
        ),
        migrations.AddField(
            model_name='busv2',
            name='transformed',
            field=models.NullBooleanField(default=False, verbose_name=b'Transformed'),
        ),
        migrations.AddField(
            model_name='eventforbusstop',
            name='transformed',
            field=models.NullBooleanField(default=False, verbose_name=b'Transformed'),
        ),
        migrations.AddField(
            model_name='eventforbusv2',
            name='transformed',
            field=models.NullBooleanField(default=False, verbose_name=b'Transformed'),
        ),
        migrations.AddField(
            model_name='report',
            name='transformed',
            field=models.NullBooleanField(default=False, verbose_name=b'Transformed'),
        ),
        migrations.AddField(
            model_name='reportinfo',
            name='transformed',
            field=models.NullBooleanField(default=False, verbose_name=b'Transformed'),
        ),
    ]