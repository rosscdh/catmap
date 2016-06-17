# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shelter', '0003_location_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='altitude',
            field=models.CharField(db_index=True, max_length=255, null=True, blank=True),
        ),
    ]
