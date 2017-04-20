# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from django.contrib.postgres.operations import CreateExtension


class Migration(migrations.Migration):

    dependencies = [
        ('AndroidRequests', '0906_transformation_20161102_1526'),
    ]

    operations = [
        CreateExtension('postgis'),
    ]
