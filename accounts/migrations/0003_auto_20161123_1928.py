# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-23 19:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_transantiagouser_transappuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carrier',
            name='id',
        ),
        migrations.RemoveField(
            model_name='carrieruser',
            name='id',
        ),
        migrations.RemoveField(
            model_name='transantiagouser',
            name='id',
        ),
        migrations.RemoveField(
            model_name='transappuser',
            name='id',
        ),
        migrations.AlterField(
            model_name='carrier',
            name='color_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='carrieruser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transantiagouser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transappuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]