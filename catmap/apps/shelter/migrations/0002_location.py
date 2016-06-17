# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shelter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(db_index=True, max_length=255, null=True, blank=True)),
                ('jurisdiction', models.CharField(db_index=True, max_length=255, null=True, blank=True)),
                ('lat', models.CharField(db_index=True, max_length=255, null=True, blank=True)),
                ('lon', models.CharField(db_index=True, max_length=255, null=True, blank=True)),
            ],
        ),
    ]
