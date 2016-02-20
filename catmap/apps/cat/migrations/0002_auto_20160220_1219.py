# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cat',
            name='fake_date_event',
            field=models.DateField(null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='cat',
            name='sex',
            field=models.CharField(blank=True, max_length=3, null=True, choices=[(b'm', b'Male'), (b'f', b'Female')]),
        ),
    ]
